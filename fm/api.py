# apy with retry


### core pattern:
from ast import TypeVar
from curses import wrapper
from typing import Any, Callable
import time

from pydantic.networks import MAX_EMAIL_LENGTH



T = TypeVar

def call_with_retry(
        fn: Callable[[],T],
        max_attempts: int = 3,
        base_delay: float = 1.0,
) -> T:

    last_exception = None
    for attempt in range(max_attempts):
            try:
                return fn()
            except Exception as e:
                last_exception = e
                if attempt == max_attempts - 1:
                    raise

                delay = base_delay * ( 2 ** attempt )
                time.sleep(delay)

    raise last_exception



#--- fm: yep all good and in good time 


### Var 1 decorator version


def retry(max_attempts: int = 3, base_delay: float = 1.0):


        def decorator(fn: Callable[..., T]) -> Callable[..., T]:  # forgot fn: 

            @wraps(fn)
            def wrapper(*args, **kwargs) -> T:
                return call_with_retry(
                    lambda: fn(*args, **kwargs),
                    max_attempts = max_attempts,
                    base_delay = base_delay,
                )
            return wrapper
        return decorator

### fm: ok 


#### var 2 with specific exceptions


def retry_with_specific(
    fn: Callable[[], T],
    exceptions: tuple[Exception[type],...],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> T: 



        for attempt in range(max_attempts):

            try:
                return fn()

            except exceptions as e:
                if attempt == max_attempts -1:
                    raise

                delay = base_delay * (2 ** attempt)
                time.sleep(delay)

        raise RuntimeError("Unreachable")

# --- fm: ok 


### with jitter



def with_jitter(
    fn: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    jitter: float = 0.5,
) -> T:


    for attempt in range(max_attempts):
        try:
            return fn()

        except Exception:

            if attempt == max_attempts -1:
                raise

            jittered_delay = (base_delay * (2**attempt)* (1+ random.uniform(-jitter, jitter)))
            time.sleep(jittered_delay)

    raise RuntimeError("Unrachable")


### --- FM: ok


### with callback logging



def retry_with_callback(
    fn: Callable[[], T],
    on_retry: Callable[int, str],   # || this was close: on_retry: Callable[[int, str], None] | None = None
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> T:


    for attempt in range(max_attempts):
        try:
            return fn()

        except Exception as e:

            if attempt == max_attempts - 1:
                raise

            if on_retry:
                on_retry(attempt +1, e)

            delay = base_delay * ( 2 ** attempt)
            time.sleep(delay)

    raise RuntimeError("Unreachable")


# --- fm: a thing about defining the functs arg on_retry but overall quite ok


### async version


async def async_version(
    fn: Callable[..., Any],  # ||| this should be fn: Callable[[], Any]:
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> Any: 

    import asyncio
    for attempt in range(max_attempts):
        try:
            result = fn()

            if asyncio.iscoroutine(result):
                return await result

            else:
                return result
        except Exception:

            if attempt == max_atempts -1:
                raise

            delay = base_delay * ( 2 ** attempt) # OMG DUDE WTF THIS IS ASYNC WAKE THE FUCK UP
            time.sleep(delay)

    raise RuntimeError("Unreachable")

### --- fM: fuck you'll have to do resp now --- 



# 1: 


async def async_call(
    fn: Callable[[], Any],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> Any:



    import asyncio
    for attempt in range(max_attempts):
        try:
            result = fn()

            if asyncio.iscoroutine(result):
                return await result
            return result

        except Exception:

            if attempt == max_attempts -1: 
                raise

            await asyncio.sleep(base_delay*(2**attempt))

    raise RuntimeError("unreachable")




# 2:


async def async_call(
    fn: Callable[[], Any],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> Any:


    import asyncio
    for attempt in rage(max_attempts):
        try:
            result = fn()

            if asyncio.iscoroutine(result):
                return await result

            return result

        except Exception:

            if attempt == max_attempts -1:
                raise

            await asyncio.sleep(base_delay*(2**attempt))

    raise RuntimeError("unreachabl")

#### ---- problems 


### 1: basic retry



def call_with_retry(
    fn: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> Any:

    last_exception = None
    for attempt in range(max_attempts):
        try:
            return fn()

        except Exception as e:
            last_exception = e

            if attempt == max_attempts -1:
                raise

            delay = base_delay * (2**attempt)
            time.sleep(delay)

    raise last_exception

# --- fm: 3 mins - V: yep thumbs up


### 2: decorator



def retry(max_attempts: int = 3, base_delay: float = 1.0):


    def decorator(fn: Callable[[], T]) -> Callable[[], T]:

        @wraps(fn)
        def wrapper(*args, **kwargs) -> T:
            return call_with_retry(
                lambda: fn(*args, **kwargs),
                max_attempts = max_attempts,
                base_delay = base_delay,
            )
        return wrapper
    return decorator

### --- fm: great stuff 


### 3: with specific exceptions



def call_with_specific_exceptions(
    fn: Callable[[], T],
    exceptions: list[str],   ### ||| yes exceptions is a tuple tuple[type[Exception], ...]
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> T:

    for attempt in range(max_attempts):

        try:
            return fn()

        except exceptions as e:
            if attempt == max_attempts -1:
                raise

            time.sleep(base_delay * (2**attempt))

    raise RuntimeError("Unreachable")

### --- fm: 3-5 mins - V: ok except exceptions 


### 4 with jitter



def call_with_jitter(
    fn: Callable[[], T],
    max_attempts: int = 3,
    base_delay: flaot = 1.0,
    jitter: float = 0.5,
) -> T:

    import random
    for attempt in range(max_attempts):
        try:
            return fn()

        except Exception:

            if attempt == max_attempts -1:
                raise

            delay = base_delay * (2**attempt)
            jittered_delay = delay * (1 + random.uniform(-jitter, jitter))
            time.sleep(jittered_delay)

    raise RuntimeError("Unreachable")


# fm: yeah shits fine 


### 5 async version


async def async_call(
    fn: Callable[[], Any],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> Any:

    import asyncio

    for attempt in range(max_attempts):
        try:
            result = fn()

            if asyncio.iscoroutine(result):
                return await result
            return result

        except Exception:

            if attempt == max_attempts -1:
                raise

            await asyncio.sleep(base_delay*(2**attempt))

    return RuntimeError("unreachable")

### fm: yep ok 



        