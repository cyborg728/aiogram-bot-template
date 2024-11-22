# from sqlalchemy.exc import IntegrityError

# async def integrity_error_get_key(exception: IntegrityError) -> str:
#     try:
#         return getattr(exception.__cause__.__cause__, "constraint_name")
#     except AttributeError:
#         return getattr(exception.__cause__.__cause__, "column_name", None)
