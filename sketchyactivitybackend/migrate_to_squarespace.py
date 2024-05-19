import selenium
import json

# Use selenium to add projects individually to squarespace
# (since squarespace doesn't have an API)

# 1. Go to squarespace
# 2. Login
# 3. Go to projects
# 4. Add project
# 5. Fill out project details
# 6. Save project
# 7. Repeat steps 4-6 for each project
# 8. Logout


class SquareSpaceProjectUploader:
    def __init__(self):
        pass

    def upload_project(self):
        pass

    def get_projects(self):
        """return list of projects each with structure"""
        with open("porfolio.json", "r") as f:
            return json.load(f)
