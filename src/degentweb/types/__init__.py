"""Convenience type aliases."""

from typing import Callable, Coroutine

Fn = Callable
type Fut[T] = Coroutine[None, None, T]
