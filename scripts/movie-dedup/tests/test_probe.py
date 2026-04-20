"""Bucket classification boundaries."""

from movie_dedup.probe import Bucket, classify


def test_sd_boundary():
    assert classify(1199) is Bucket.SD
    assert classify(1200) is Bucket.HD


def test_hd_boundary():
    assert classify(1799) is Bucket.HD
    assert classify(1800) is Bucket.FULL_HD


def test_fullhd_boundary():
    assert classify(3199) is Bucket.FULL_HD
    assert classify(3200) is Bucket.FOUR_K


def test_extreme_values():
    assert classify(0) is Bucket.SD
    assert classify(7680) is Bucket.FOUR_K


def test_bucket_rank_order():
    assert Bucket.SD.rank < Bucket.HD.rank < Bucket.FULL_HD.rank < Bucket.FOUR_K.rank
