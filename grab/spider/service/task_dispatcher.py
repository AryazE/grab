from __future__ import annotations

from queue import Empty, Queue
from typing import Any, Callable, Optional

from ..interface import FatalErrorQueueItem
from ..task import Task
from .base import BaseService, ServiceWorker


class TaskDispatcherService(BaseService):
    def __init__(
        self,
        fatal_error_queue: Queue[FatalErrorQueueItem],
        process_service_result: Callable[[Any, Task, Optional[dict[str, Any]]], Any],
    ):
        super().__init__(fatal_error_queue)
        self.process_service_result = process_service_result
        self.input_queue: Queue[Any] = Queue()
        self.worker = self.create_worker(self.worker_callback)
        self.register_workers(self.worker)

    def start(self) -> None:
        self.worker.start()

    def worker_callback(self, worker: ServiceWorker) -> None:
        while not worker.stop_event.is_set():
            worker.process_pause_signal()
            try:
                result, task, meta = self.input_queue.get(True, 0.1)
            except Empty:
                pass
            else:
                self.process_service_result(result, task, meta)
