import requests


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
        return response.json()
    return None


if __name__ == "__main__":
    cid = "10503000532"
    owner_id = fetch_ownerid_by_cid(cid)
    if owner_id:
        print(f"Owner ID for CID {cid}: {owner_id}")
    else:
        print(f"Owner ID not found for CID {cid}")
