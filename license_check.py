# sketchy basic licensing module
# Pop-up for license input
# Store license file somewhere (do super basic obfuscating/encrypt for fun)
# Logic for checking if license is valid or trial is not expired

import requests
def get_license_status():
        # Barebones license check. Check by polling webpage if the trial is activated.
        try:
            r = requests.get("https://proxybeuker.com/license2.html", timeout=4)
            if r.status_code == 200:
                return True
            else:
                return False

        except requests.exceptions.RequestException:
            return False