import requests


class OwnerDetails:
    def __init__(self, data):
        self.ownerId = data.get("id")
        self.name = data.get("name")
        self.dob = data.get("dateOfBirth")
        self.gender = data.get("gender")
        self.avatarUrl = data.get("avatarUrl")
        self.contact = data.get("mobileNo")


def fetch_ownerid_by_cid(cid: str):
    url = f"https://api.eralis.rsta.gov.bt/svc/driving-license/api/licenses/search-by-cid/{cid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("ownerId")
    return None


def fetch_details_by_owner_id(ownerId: str):
    url = f"https://api.eralis.rsta.gov.bt/svc/personal-information/api/personal-informations/{ownerId}"
    response = requests.get(url)
    if response.status_code == 200:
        ownerData = OwnerDetails(response.json())
        return ownerData
    return None


if __name__ == "__main__":
    cid = "10503000532"
    owner_id = fetch_ownerid_by_cid(cid)
    if owner_id:
        owner_details = fetch_details_by_owner_id(owner_id)
        if owner_details:
            print(f"Owner Details for CID {cid}:")
            print(f"ID: {owner_details.ownerId}")
            print(f"Name: {owner_details.name}")
            print(f"Date of Birth: {owner_details.dob}")
            print(f"Gender: {owner_details.gender}")
            print(f"Avatar URL: {owner_details.avatarUrl}")
            print(f"Contact: {owner_details.contact}")
        else:
            print(f"Owner details not found for Owner ID {owner_id}")
    else:
        print(f"Owner ID not found for CID {cid}")
