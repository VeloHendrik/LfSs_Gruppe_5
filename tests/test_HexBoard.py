from env.HexBoard import Tile, Grid
import pytest

def test_Tile_create_Tile():
    """
    Implicitly tests computeDimensions()
    """
    tile = Tile(0,0,10)
    assert tile.gridPosition == (0,0)
    assert tile.width == 10*3**0.5
    assert tile.height == 20

def test_Tile_corner_Points():
    """
    Implicitly tests cornerPoint() and centerPoint()
    :return:
    """
    tile = Tile(0,0,10)
    cornerPoints = tile.cornerPoints()
    assert len(cornerPoints) == 6
    assert cornerPoints[0][0] == pytest.approx(cornerPoints[-1][0])

def test_Grid_create_Grid():
    grid = Grid(10,10,10)
    assert sum(grid.visitedTiles.values()) == 0
