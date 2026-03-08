from handlers.tasks import router as trouter
from handlers.ping import router as prouter
from handlers.user import router as urouter
from handlers.auth import router as arouter
routers = [trouter, prouter, urouter, arouter]