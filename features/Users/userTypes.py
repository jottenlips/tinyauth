from ariadne import load_schema_from_path, ObjectType, QueryType, MutationType
from features.Users.user import verify_user, send_verification, get_me


userQueries = QueryType()
userMutations = MutationType()

userTypes = load_schema_from_path("./features/Users/user.gql")
userObjectType = ObjectType('TAUser')
userQueries.set_field('getMe', get_me)
userMutations.set_field('sendVerification', send_verification)
userMutations.set_field('verifyUser', verify_user)
