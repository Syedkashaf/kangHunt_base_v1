import asyncio
import json
import os
import re
from models.schemas import PluginResponse
from .base_plugin import BaseOSINTPlugin

class GHuntPlugin(BaseOSINTPlugin):
    def __init__(self):
        self.source_name = "GHunt (Autonomous Engine)"

    async def execute(self, target: str) -> PluginResponse:
        temp_json = f"ghunt_state_{hash(target)}.json"
        temp_txt = f"ghunt_dump_{hash(target)}.txt"
        
        try:
            # -------------------------------------------------------------
            # THE NUCLEAR FIX: NATIVE SHELL REDIRECTION
            # -------------------------------------------------------------
            # Python pipes bypass kar ke direct OS-level shell command use kar rahe hain
            # taake crash hone se pehle ka har ek harf (character) text file mein save ho.
            command = f"ghunt email {target} --json {temp_json} > {temp_txt} 2>&1"
            
            process = await asyncio.create_subprocess_shell(command)
            await asyncio.wait_for(process.communicate(), timeout=120.0)
            
            output_text = ""
            # File se native text read karna (No buffer drops)
            if os.path.exists(temp_txt):
                with open(temp_txt, 'r', encoding='utf-8', errors='ignore') as f:
                    output_text = f.read()
                os.remove(temp_txt)
            
            # ANSI Cleaning (Remove invisible color codes)
            clean_text = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', output_text)
            
            regex_intel = {}
            gaia_match = re.search(r'Gaia ID\s*:\s*(\d+)', clean_text, re.IGNORECASE)
            if gaia_match:
                regex_intel["gaia_id"] = gaia_match.group(1)
                
            avatar_match = re.search(r'=>\s*(https://[^\s]+)', clean_text)
            if avatar_match:
                regex_intel["profile_photo"] = avatar_match.group(1)
                
            maps_match = re.search(r'Profile page\s*:\s*(https://www\.google\.com/maps[^\s]+)', clean_text, re.IGNORECASE)
            if maps_match:
                regex_intel["maps"] = True
                regex_intel["maps_reviews_url"] = maps_match.group(1)
                
            yt_match = re.search(r'Channel link\s*:\s*(https://www\.youtube\.com/[^\s]+)', clean_text, re.IGNORECASE)
            if yt_match:
                regex_intel["youtube"] = True
                
            services_section = re.search(r'Activated Google services\s*:\n((?:\s*-\s*.+\n)+)', clean_text, re.IGNORECASE)
            if services_section:
                services = re.findall(r'-\s*(.+)', services_section.group(1))
                for srv in services:
                    regex_intel[srv.lower().strip()] = True

            # Data Merge Logic
            if os.path.exists(temp_json):
                with open(temp_json, 'r', encoding='utf-8') as file:
                    raw_intelligence = json.load(file)
                os.remove(temp_json)
                
                for key, value in regex_intel.items():
                    raw_intelligence[key] = value
                        
                return PluginResponse(
                    source_name=self.source_name,
                    status="success",
                    raw_data=raw_intelligence,
                    message="Deep footprints mapped via JSON + Native Shell Extraction."
                )
            else:
                # -------------------------------------------------------------
                # THE SALVAGE OPERATION (Rescuing data from the Text Dump)
                # -------------------------------------------------------------
                if regex_intel:
                    return PluginResponse(
                        source_name=self.source_name,
                        status="success", 
                        raw_data=regex_intel,
                        message="API crashed (Timeout), but data natively salvaged via OS Shell Redirection."
                    )
                
                return PluginResponse(
                    source_name=self.source_name,
                    status="failed",
                    message="Subprocess bypassed: JSON crashed and shell scraping yielded no target data."
                )
                
        except asyncio.TimeoutError:
            if os.path.exists(temp_json): os.remove(temp_json)
            if os.path.exists(temp_txt): os.remove(temp_txt)
            return PluginResponse(source_name=self.source_name, status="failed", message="Timeout occurred.")
        except Exception as e:
            if os.path.exists(temp_json): os.remove(temp_json)
            if os.path.exists(temp_txt): os.remove(temp_txt)
            return PluginResponse(source_name=self.source_name, status="error", message=f"Engine Fault: {str(e)}")
