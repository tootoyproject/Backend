from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if code == 400:
            code = response.status_code
            response.data['status'] = code
            response.data['msg'] = '게시글 작성에 실패하셨습니다.'
        elif code == 304:
            response.data['status'] = 400
            response.data['msg'] = '게시글 수정에 실패하셨습니다.'
        elif code == 404:
            response.data['status'] = 400
            response.data['msg'] = '해당 게시글은 없는 게시물입니다.'
    return response