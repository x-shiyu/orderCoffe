from django.http.response import HttpResponse

def loginCheck(view_fn,*args, **kwargs):
    def auth(req,*args, **kwargs):
      if req.user.is_authenticated==False:
        response = HttpResponse()
        response.status_code = 401
        return  response
      else:
        return view_fn(req)
    return auth