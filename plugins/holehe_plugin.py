import asyncio
from models.schemas import PluginResponse
from .base_plugin import BaseOSINTPlugin

class HolehePlugin(BaseOSINTPlugin):
    def __init__(self):
        self.source_name = "Holehe (Account Footprint)"

    async def execute(self, target: str) -> PluginResponse:
        try:
            # Asynchronous Subprocess Execution
            # '--only-used' sirf woh sites dikhata hai jahan account bana ho
            # '--no-color' terminal color codes (jaise \033[92m) ko remove karta hai taake text clean rahe
            process = await asyncio.create_subprocess_exec(
                "holehe", target, "--only-used", "--no-color",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Holehe 120+ sites scan karta hai, isliye hum 30 seconds ka timeout de rahe hain
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30.0)
            
            # Output ko bytes se string mein convert karna
            output = stdout.decode('utf-8')
            
            # Parsing the Output (Extracting sites and masked data)
                        # ... (upar wala subprocess code wesa hi rahega) ...

            # Parsing the Output (Extracting sites and masked data)
            found_accounts = []
            
            for line in output.split('\n'):
                # THE FIX: Hum check kar rahe hain ke line mein '[+]' ho, 
                # LEKIN usme "Email used" (jo legend ka hissa hai) NA ho.
                if "[+]" in line and "Email used" not in line:
                    clean_line = line.replace("[+]", "").strip()
                    # Sirf non-empty strings ko add karein
                    if clean_line:
                        found_accounts.append(clean_line)
                    
            return PluginResponse(
                source_name=self.source_name,
                status="success",
                raw_data={
                    "total_found": len(found_accounts),
                    "accounts_and_numbers": found_accounts
                },
                message="Password recovery footprinting complete."
            )
            
        except asyncio.TimeoutError:
            # ... (neeche wala error handling code wesa hi rahega) ...

            return PluginResponse(
                source_name=self.source_name,
                status="failed",
                message="Timeout Error: The scan took longer than 30 seconds."
            )
        except Exception as e:
            return PluginResponse(
                source_name=self.source_name,
                status="error",
                message=f"Subprocess Error: {str(e)}"
            )