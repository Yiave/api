# coding=utf-8
from flask import request, current_app, url_for, jsonify, json
from flask import Response
from flask import Flask, make_response
from functools import wraps
import flask
from flask import render_template, redirect
from ..aaa import errors
from .models import Wish, Cobuy
from ..promotion.models import Promotion
from . import cobuy


# TODO: get_distance + optimise + punish factor
def get_distance_by_clothing(min_time, max_time, wish_start_time, wish_end_time):
    '''
    :param min_time 目标Wish的开始时间
    :param max_time 目标Wish的结束时间
    :param wish_start_time 测试/待匹配数据集
    :param wish_end_time 测试/待匹配数据集
    '''
    distance = None

    if wish_end_time < min_time:  # 完全左
        distance = (wish_start_time - min_time) + (wish_end_time - min_time)
    elif wish_start_time < min_time < wish_start_time < max_time:  # 左包含
        distance = (wish_start_time - min_time) + (wish_end_time - min_time)
    elif min_time < wish_start_time < wish_start_time < max_time:  # 完全包含
        distance = (wish_end_time - wish_start_time)
    elif min_time < wish_start_time < max_time < wish_end_time:  # 右包含
        distance = (max_time - wish_end_time) + (max_time - wish_start_time)
    elif max_time < wish_start_time:  # 完全右
        distance = (max_time - wish_end_time) + (max_time - wish_start_time)
    elif wish_start_time < min_time < max_time < wish_end_time:  # 完全外包含
        distance = (min_time - wish_start_time) + (max_time - wish_end_time)

    return distance


def recomendate_wish_by_clothing(wish):
    # 1. recomentdate via Wish Time
    max_time = wish.wish_time_start
    min_time = wish.wish_time_end

    wishs = Wish.query.filter(Wish.promotion_id == id, Wish.is_matched == False, Wish.is_open == True).all()

    dataset = dict()
    for w in wishs:
        wish_start_time = w.wish_time_start
        wish_end_time = w.wish_time_end

        distance = get_distance_by_clothing(min_time, max_time, wish_start_time, wish_end_time)

        dataset[w.id] = distance

    dataset.values().sort(reverse=True)

    # TODO: 2. recomendte via wish count

    return dataset


def recomendate_cobuy_by_clothing(wish):
    # 1. recomentdate via Wish Time
    max_time = wish.wish_time_start
    min_time = wish.wish_time_end

    cobuys = Cobuy.query.filter(Cobuy.promotion_id == id, Wish.is_matched == False, Wish.is_open == True).all()

    dataset = dict()
    for w in cobuys:
        wish_start_time = w.wish_time_start
        wish_end_time = w.wish_time_end

        distance = get_distance_by_clothing(min_time, max_time, wish_start_time, wish_end_time)

        dataset[w.id] = distance

    dataset.values().sort(reverse=True)

    # TODO: 2. recomendte via wish count

    return dataset


@cobuy.route("/promotions/<int:id>/wish/clothing", methods=["POST"])
def create_wish_by_clothing(id):
    data = request.get_json()
    promotion_id = id
    customer_id = data["customer_id"]
    wish_count = data["wish_count"]
    wish_time_start = data["wish_time_start"]
    wish_time_end = data["wish_time_end"]
    match_type = data["match_type"]

    promotion = Promotion.query.get(id)

    # add wish
    wish = Wish.from_json(data)
    wish.promotion_id = promotion_id

    if match_type == 0:  # System Match
        # TODO: system match backend function
        wish.add(wish)

        wish_data = recomendate_wish_by_clothing(wish)
        coby_data = recomendate_cobuy_by_clothing(wish)
        return jsonify({"wish": wish_data, "cobuy": coby_data})

    elif match_type == 1:  # User Create Match
        wish.is_open = False
        wish.add(wish)

        cobuy = Cobuy(wish_id=wish.id, promotion_id=wish.promotion_id, customer_id=wish.customer_id,
                      match_type=wish.match_type, end_time=promotion.end_time, min_time=wish_time_start,
                      max_time=wish_time_end)
        cobuy.add(cobuy)
        return jsonify(cobuy.to_json())


@cobuy.route("/cobuy/recomwish/system/clothing", methods=["POST"])
def create_clothing_cobuy_by_system_recomwish():
    pass


@cobuy.route("/cobuy/<int:id>/userjoin", methods=['POST'])
def create_cobuy_by_userjoin(id):
    data = request.get_json()
    customer_id = data["customer_id"]
    wish_count = data["wish_count"]
    match_type = 2

    cobuy = Cobuy.query.get(id)
    if not cobuy:
        return errors.notfound("Cobuy " + str(id) + " not found.")

    # add wish
    wish_time_start = cobuy.min_time
    wish_time_end = cobuy.max_time
    wish = Wish(promotion_id=cobuy.promotion_id, customer_id=customer_id, wish_count=wish_count,
                match_type=match_type, wish_time_start=wish_time_start, wish_time_end=wish_time_end)
    wish.add(wish)

    # add cobuy
    cobuy = Cobuy(wish_id=wish.id, promotion_id=wish.promotion_id, customer_id=wish.customer_id,
                  match_type=wish.match_type, end_time=cobuy.end_time, min_time=wish_time_start,
                  max_time=wish_time_end)
    cobuy.add(cobuy)

    return jsonify(cobuy.to_json())


@cobuy.route("/wish/<int:id>/open", methods=["PUT", "PATCH"])
def update_wish_open(id):
    wish = Wish.query.get(id)

    if not wish:
        return errors.notfound("Wish " + str(id) + " not found.")

    wish.update_open(True)

    return jsonify(wish.to_json())


@cobuy.route("/promotions/<int:id>/wish", methods=["GET"])
def get_wish(id):
    wishs = Wish.query.filter(Wish.promotion_id == id, Wish.is_matched == False, Wish.is_open == True).all()

    return


@cobuy.route("/promotions/<int:id>/wish/consume", methods=["POST"])
def create_wish_by_consume(id):
    pass


if __name__ == '__main__':
    pass
