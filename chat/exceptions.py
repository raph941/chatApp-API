from rest_framework.exceptions import APIException
from rest_framework import status


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ('Could not satisfy the request Accept header.')
    default_code = 'not_acceptable'



if __name__ == "__main__":
    raise CustomException
