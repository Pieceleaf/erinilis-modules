from nonebot import *
from . import query, util
from hoshino import Service  # 如果使用hoshino的分群管理取消注释这行

#
sv = Service('ys-user')  # 如果使用hoshino的分群管理取消注释这行
# 初始化配置文件
config = util.get_config()

# 初始化nonebot
_bot = get_bot()

db = util.init_db(config.cache_dir)


@sv.on_message('group')  # 如果使用hoshino的分群管理取消注释这行 并注释下一行的 @_bot.on_message("group")
# @_bot.on_message  # nonebot使用这
async def main(*params):
    bot, ctx = (_bot, params[0]) if len(params) == 1 else params
    uid = ctx.user_id
    msg = str(ctx['message']).strip()
    keyword = util.get_msg_keyword(config.comm.player_uid, msg, True)
    if isinstance(keyword, str):
        if not keyword:

            info = db.get(uid, {})
            if not info:
                return await bot.send(ctx, '请输入游戏uid, 只支持b服或者官服, 只需要输入一次就会记住下次直接使用%s获取就好' % config.comm.player_uid)
            else:
                keyword = info['uid']

        await bot.send(ctx, await get_stat(keyword))
        db[uid] = {'uid': keyword}


async def get_stat(uid):
    if not uid.isdigit():
        return '只能是数字ID啦'
    info = query.info(uid)
    if info.retcode != 0:
        return '[%s]错误或者不存在 (%s)' % (uid, info.message)
    stats = query.stats(info.data.stats, True)
    msg = 'UID: %s\n%s\n' % (uid, stats.string)
    for i in info.data.world_explorations:
        msg += '\n%s的探索进度为%s，声望等级为：%s级' % (i["name"], str(i["exploration_percentage"] / 10) + '%', i["level"])
    return msg
