import requests
import csv
from datetime import datetime


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


def get_owner_detail_by_cid(cid: str):
    owner_id = fetch_ownerid_by_cid(cid)
    if owner_id:
        owner_details = fetch_details_by_owner_id(owner_id)
        return owner_details
    return None


def calculate_age(dob: str):
    if not dob or dob == "Not Found":
        return None
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        return age
    except ValueError:
        return None


if __name__ == "__main__":
    file_name = "data/test.csv"
    output_file = "data/output.csv"

    with open(output_file, mode="w", newline="") as writefile:
        csv_writer = csv.writer(writefile)
        csv_writer.writerow(
            [
                "cid",
                "name",
                "dob",
                "age",
                "gender",
                "avatarUrl",
                "contactRsta",
                "contact_50%",
                "contact_20%",
                "noUnits",
                "buildingIds",
                "plotIds",
            ]
        )
        with open(file_name, mode="r") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                owner_data = get_owner_detail_by_cid(row[2])
                if owner_data:
                    csv_writer.writerow(
                        [
                            row[2],
                            owner_data.name,
                            owner_data.dob,
                            calculate_age(owner_data.dob),
                            owner_data.gender,
                            f"https://s3.eralis.rsta.gov.bt/eralis{owner_data.avatarUrl}",
                            owner_data.contact,
                            row[3],
                            row[4],
                            row[5],
                            row[6],
                            row[7],
                        ]
                    )
                else:
                    csv_writer.writerow(
                        [
                            row[2],
                            "Not Found",
                            "Not Found",
                            "Not Found",
                            "Not Found",
                            "Not Found",
                            "Not Found",
                            row[3],
                            row[4],
                            row[5],
                            row[6],
                            row[7],
                        ]
                    )
