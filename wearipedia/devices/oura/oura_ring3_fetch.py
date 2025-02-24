import requests

__all__ = ["fetch_real_data"]


def fetch_real_data(data_type, access_token, start_date, end_date):
    """Main function for fetching real data from the Oura Ring API.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :param data_type: the type of data to fetch, one of "Personal Info", "Heart Rate", "Sessions", "Tags", "Workouts", "Daily Sleep", "Daily Activity", "Daily Readiness", "Ideal Bedtime"
    :param access_token: access token for the API
    :return: the data fetched from the API according to the inputs
    :rtype: List
    """

    def call_api_version_2(
        url: str,
        start_date=start_date,
        end_date=end_date,
        access_token=access_token,
        start_date_col: str = "start_date",
        end_date_col: str = "end_date",
        call: str = "GET",
    ):
        """
        Second version of the api, the only supported API version as of 1/24/25
        """
        headers = {"Authorization": "Bearer " + access_token}
        params = {start_date_col: start_date, end_date_col: end_date}

        response = requests.request(call, url=url, headers=headers, params=params)

        # Handle specific HTTP status codes
        if response.status_code != 200:
            error_msg = f"{response.status_code}"
            try:
                error_detail = response.json()
                if isinstance(error_detail, dict):
                    error_msg = f"{error_msg} - {error_detail.get('detail', '')}"
            except:
                pass

            raise Exception("Request failed with error: " + error_msg)
        return response.json()

    # heart_rate
    heart_rate = call_api_version_2(
        url="https://api.ouraring.com/v2/usercollection/heartrate",
        start_date_col="start_datetime",
        end_date_col="end_datetime",
        start_date=start_date + "T00:00:00-23:59",
        end_date=end_date + "T00:00:00-23:59",
    )

    # personal_info
    personal_info = call_api_version_2(
        url="https://api.ouraring.com/v2/usercollection/personal_info"
    )

    # sessions
    sessions = call_api_version_2(
        url="https://api.ouraring.com/v2/usercollection/sessions"
    )

    # tag
    tag = call_api_version_2(url="https://api.ouraring.com/v2/usercollection/tag")

    # workout
    workout = call_api_version_2(
        url="https://api.ouraring.com/v2/usercollection/workout"
    )

    # daily_activity
    daily_activity = call_api_version_2(
        url="https://api.ouraring.com/v2/usercollection/daily_activity"
    )

    # daily_sleep
    daily_sleep = call_api_version_2(
        url="https://api.ouraring.com/v2/usercollection/daily_sleep"
    )

    # sleep
    sleep = call_api_version_2(url="https://api.ouraring.com/v2/usercollection/sleep")

    # readiness
    readiness = call_api_version_2(
        url="https://api.ouraring.com/v2/usercollection/daily_readiness"
    )

    # ideal_bedtime
    ideal_bedtime = call_api_version_2(
        url="https://api.ouraring.com/v2/usercollection/sleep_time"
    )

    # aggregate data for version 2 endpoints
    api_data = dict()
    api_data["heart_rate"] = heart_rate["data"]
    api_data["personal_info"] = [personal_info]
    api_data["sessions"] = (
        sessions["detail"] if sessions["detail"] != "Not Found" else [{}]
    )
    api_data["tag"] = tag["data"] if tag["data"] else [{}]
    api_data["workout"] = workout["data"] if workout["data"] else [{}]
    api_data["daily_activity"] = (
        daily_activity["data"] if daily_activity["data"] else [{}]
    )

    api_data["sleep"] = sleep["data"]
    api_data["daily_sleep"] = daily_sleep["data"]
    api_data["readiness"] = readiness["data"]
    api_data["ideal_bedtime"] = ideal_bedtime["data"]

    return api_data[data_type]
