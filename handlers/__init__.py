from handlers.tasks import router as trouter
from handlers.ping import router as prouter
from handlers.user import router as urouter
from handlers.auth import router as arouter
from handlers.notes import router as nrouter
from handlers.ui import router as uirooter

routers = [uirooter, trouter, prouter, urouter, arouter, nrouter]
