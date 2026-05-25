from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

router = APIRouter()


class ConnectionManager:

    def __init__(self):

        self.active_connections = []

    async def connect(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections.append(
            websocket
        )

    def disconnect(
        self,
        websocket: WebSocket
    ):

        self.active_connections.remove(
            websocket
        )

    async def broadcast(
        self,
        message: dict
    ):

        for connection in self.active_connections:

            await connection.send_json(
                message
            )


manager = ConnectionManager()


@router.websocket("/ws/logs")
async def websocket_logs(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )