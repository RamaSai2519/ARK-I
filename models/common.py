from shared.models.constants import TimeFormats
from shared.configs import CONFIG as config
from shared.models.interfaces import Output
from datetime import datetime, timedelta
import requests
import pytz


class CommonTools:
    def __init__(self):
        pass

    @staticmethod
    def get_current_time() -> str:
        times = {
            'TODAY_IST': datetime.now(pytz.timezone('Asia/Kolkata')),
            'TODAY_UTC': datetime.now(pytz.utc),
            'TOMORROW_IST': (datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=1)),
            'TOMORROW_UTC': (datetime.now(pytz.utc) + timedelta(days=1)),
        }
        times = {key: value.strftime(TimeFormats.ANTD_TIME_FORMAT)
                 for key, value in times.items()}
        response = "Current IST Time: "
        response += times['TODAY_IST']
        response += "\nCurrent UTC Time: "
        response += times['TODAY_UTC']
        response += "\nTomorrow IST Time: "
        response += times['TOMORROW_IST']
        response += "\nTomorrow UTC Time: "
        response += times['TOMORROW_UTC']
        return response

    @staticmethod
    def get_user_details(phoneNumber: str) -> dict:
        url = config.URL + '/actions/user'
        params = {'phoneNumber': phoneNumber}
        response = requests.get(url, params=params)
        output = Output(**response.json())
        user = output.output_details

        data = {
            '_id': user.get('_id', ''),
            'name': user.get('name', ''),
            'city': user.get('city', ''),
            'refSource': user.get('refSource', ''),
            'persona': user.get('customerPersona', ''),
        }
        birthDate = user.get('birthDate')
        try:
            birthDate = datetime.strptime(
                birthDate, TimeFormats.ANTD_TIME_FORMAT)
            data['birthDate'] = birthDate.strftime('%Y-%m-%d')
        except:
            data['birthDate'] = ''
        return data
