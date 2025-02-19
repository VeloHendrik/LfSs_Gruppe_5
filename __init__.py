from gymnasium.envs.registration import register
from env.hex import HexEnv

__all__ = [HexEnv]

register(
    id='hex-v0',
    entry_point='hex.env:HexEnv',
)