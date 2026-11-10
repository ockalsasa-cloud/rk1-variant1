import threading
from typing import TypeVar

from fastapi import FastAPI
from pydantic import BaseModel, Field

T = TypeVar("T")


def chunk(items: list[T], size: int) -> list[list[T]]:
    if size < 1:
        raise ValueError("size must be at least 1")
    return [items[i : i + size] for i in range(0, len(items), size)]


counter = 0
lock = threading.Lock()


def worker() -> None:
    global counter
    for _ in range(100_000):
        with lock:
            counter += 1


def run_counter() -> int:
    global counter
    counter = 0
    threads = [threading.Thread(target=worker) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return counter


app = FastAPI()
next_id = 1


class Item(BaseModel):
    name: str
    price: float = Field(gt=0)
    tags: list[str] = Field(default_factory=list)


class ItemResponse(Item):
    id: int


@app.post("/items", response_model=ItemResponse)
def create_item(item: Item) -> ItemResponse:
    global next_id
    result = ItemResponse(id=next_id, **item.model_dump())
    next_id += 1
    return result


if __name__ == "__main__":
    print("Counter:", run_counter())
