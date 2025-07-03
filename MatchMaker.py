import discord
from discord.ext import commands
import asyncio
import random
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

# Mapas
MAPAS = [
    "Mirage", "Inferno", "Inferno_2016", "Inferno_2023", "Nuke", "Nuke_2016",
    "Overpass", "Vertigo", "Ancient", "Anubis", "Dust 2", "Dust_2_2017",
    "Train", "Train_2017", "Train_2013", "Cache_csgo", "Cache_2017", "Cobblestone"
]



POOLS_MAPAS = {
    "campanha": ["Mirage", "Inferno", "Nuke", "Ancient", "Anubis", "Dust 2", "Train"], # 7
    "todos": MAPAS.copy(),
    "olds": ["Inferno_2016", "Inferno_2023", "Nuke_2016", "Overpass", "Vertigo",
             "Dust_2_2017", "Train_2017", "Train_2013", "Cache_csgo", "Cache_2017", "Cobblestone"], # 11
    "campanha2": ["Mirage", "Inferno", "Nuke", "Ancient", "Anubis", "Dust 2", "Train", "Cobblestone", "Overpass", "Vertigo", "Cache"] #11
}

ORDEM_PICKBAN_POR_POOL = {
    "campanha": {
        "md1": [("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2")],

        "md3": [("ban", "time1"), ("ban", "time2"), ("pick", "time1"), ("pick", "time2"), ("ban", "time1"), ("ban", "time2")],

        "md5": [("ban", "time1"), ("ban", "time2"), ("pick", "time1"), ("pick", "time2"), ("pick", "time1"), ("pick", "time2")]
    },
    "todos": {
        "md1": [
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"),
        ],
        "md3": [
            # 17 ações: 15 bans e 2 picks (1 pick para cada time)
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("pick", "time1"), ("pick", "time2"),
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1")
        ],
        "md5": [
            # 17 ações: 13 bans e 4 picks (2 picks por time)
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),

            ("pick", "time1"), ("pick", "time2"),

            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),

            ("pick", "time1"), ("pick", "time2"),

            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"), ("ban", "time1")
        ]
    },
    "olds": {
        "md1": [
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2"),
        ],
        "md3": [
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("pick", "time1"), ("pick", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2")
        ],
        "md5": [
            ("ban", "time1"), ("ban", "time2"), ("pick", "time1"), ("pick", "time2"),
            ("ban", "time1"), ("ban", "time2"), ("pick", "time1"), ("pick", "time2"),
            ("ban", "time1"), ("ban", "time2")
        ]
    },
    "campanha2": {
        "md1": [
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2"),
        ],
        "md3": [
            ("ban", "time1"), ("ban", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("pick", "time1"), ("pick", "time2"), ("ban", "time1"), ("ban", "time2"),
            ("ban", "time1"), ("ban", "time2")
        ],
        "md5": [
            ("ban", "time1"), ("ban", "time2"), ("pick", "time1"), ("pick", "time2"),
            ("ban", "time1"), ("ban", "time2"), ("pick", "time1"), ("pick", "time2"),
            ("ban", "time1"), ("ban", "time2")
        ]
    }

}


EMOJIS_MAPAS = {
    "Mirage": discord.PartialEmoji(name="mirage", id=1388269838098759740),
    "Inferno": discord.PartialEmoji(name="inferno", id=1388269898576433295),
    "Nuke": discord.PartialEmoji(name="nuke", id=1388269892481843354),
    "Overpass": discord.PartialEmoji(name="overpass", id=1388269906298146927),
    "Vertigo": discord.PartialEmoji(name="vertigo", id=1388269896785465436),
    "Ancient": discord.PartialEmoji(name="ancient", id=1388269904012247110),
    "Anubis": discord.PartialEmoji(name="anubis", id=1388269907853967410),
    "Dust 2": discord.PartialEmoji(name="dust2", id=1388269901587677235),
    "Train": discord.PartialEmoji(name="train", id=1388269894700765256),
    "Cache": discord.PartialEmoji(name="cache", id=1388277066624929882),
    "Cobblestone": discord.PartialEmoji(name="cobblestone", id=1388277082135466075),

    "Inferno_2016": discord.PartialEmoji(name="inferno_2016", id=1389738277757648978),
    "Inferno_2023": discord.PartialEmoji(name="inferno_2023", id=1389738322724655306),
    "Nuke_2016": discord.PartialEmoji(name="nuke_2016", id=1389738350675496990),
    "Dust_2_2017": discord.PartialEmoji(name="dust2_2017", id=1389738378487922858),
    "Train_2017": discord.PartialEmoji(name="train_2017", id=1389738426042945709),
    "Train_2013": discord.PartialEmoji(name="train_2013", id=1389738423690072294),
    "Cache_csgo": discord.PartialEmoji(name="cache_csgo", id=1389741490422415412),
    "Cache_2017": discord.PartialEmoji(name="cache_2017", id=1389738421823475772),
}

# IDs dos canais
BACKLOG_CHANNEL_ID = 1388341908170084435
RANKING_CHANNEL_ID = 1388326801872523355

# --------------------------
# Funções de Ranking por ID
# --------------------------

def carregar_ranking():
    if not os.path.exists("ranking.json"):
        return {}
    try:
        with open("ranking.json", "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return {}
            return json.loads(data)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def salvar_ranking(ranking):
    with open("ranking.json", "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=4)

# ... seu código anterior das funções de ranking ...

def inicializar_jogador_elo(ranking, jogador):
    jogador_id = str(jogador.id)
    if jogador_id not in ranking:
        ranking[jogador_id] = {
            "nome": jogador.display_name,
            "mapas": 0,
            "series": 0,
            "derrotas_mapas": 0,
            "derrotas_series": 0,
            "por_mapa": {},
            "elo": 1000
        }
    elif "elo" not in ranking[jogador_id]:
        ranking[jogador_id]["elo"] = 1000

def atualizar_elo_vitoria(jogador, mapas_ganhos=0, series_ganhas=0):
    ranking = carregar_ranking()
    inicializar_jogador_elo(ranking, jogador)
    jogador_id = str(jogador.id)

    elo = ranking[jogador_id]["elo"]
    elo += series_ganhas * 25
    elo += mapas_ganhos * 5
    ranking[jogador_id]["elo"] = elo
    ranking[jogador_id]["nome"] = jogador.display_name

    salvar_ranking(ranking)

def atualizar_elo_derrota(jogador, mapas_perdidos=0, series_perdidas=0):
    ranking = carregar_ranking()
    inicializar_jogador_elo(ranking, jogador)
    jogador_id = str(jogador.id)

    elo = ranking[jogador_id]["elo"]
    elo -= series_perdidas * 20
    elo -= mapas_perdidos * 5
    if elo < 0:
        elo = 0
    ranking[jogador_id]["elo"] = elo
    ranking[jogador_id]["nome"] = jogador.display_name

    salvar_ranking(ranking)


def atualizar_ranking(jogador, mapa, vencedor_serie=False):
    jogador_id = str(jogador.id)
    nome = jogador.display_name
    ranking = carregar_ranking()

    if jogador_id not in ranking:
        ranking[jogador_id] = {
            "nome": nome,
            "mapas": 0,
            "series": 0,
            "derrotas_mapas": 0,
            "derrotas_series": 0,
            "por_mapa": {}
        }

    ranking[jogador_id]["nome"] = nome

    if mapa != "":
        ranking[jogador_id]["mapas"] += 1
        if mapa not in ranking[jogador_id]["por_mapa"]:
            ranking[jogador_id]["por_mapa"][mapa] = {"vitorias": 0, "derrotas": 0}
        ranking[jogador_id]["por_mapa"][mapa]["vitorias"] += 1

    if vencedor_serie:
        ranking[jogador_id]["series"] += 1

    salvar_ranking(ranking)

def registrar_derrota(jogador, mapa, perdeu_serie=False):
    jogador_id = str(jogador.id)
    nome = jogador.display_name
    ranking = carregar_ranking()

    if jogador_id not in ranking:
        ranking[jogador_id] = {
            "nome": nome,
            "mapas": 0,
            "series": 0,
            "derrotas_mapas": 0,
            "derrotas_series": 0,
            "por_mapa": {}
        }

    ranking[jogador_id]["nome"] = nome

    if mapa != "":
        ranking[jogador_id]["derrotas_mapas"] += 1
        if mapa not in ranking[jogador_id]["por_mapa"]:
            ranking[jogador_id]["por_mapa"][mapa] = {"vitorias": 0, "derrotas": 0}
        ranking[jogador_id]["por_mapa"][mapa]["derrotas"] += 1

    if perdeu_serie:
        ranking[jogador_id]["derrotas_series"] += 1

    salvar_ranking(ranking)

# --------------------------
# Comandos de Ranking
# --------------------------

@bot.command()
async def rankingseries(ctx):
    ranking = carregar_ranking()
    if not ranking:
        await ctx.send("⚠️ Nenhum dado de ranking encontrado.")
        return

    series_ordenado = sorted(ranking.items(), key=lambda x: x[1]["series"], reverse=True)
    descricao = []
    for i, (jogador_id, dados) in enumerate(series_ordenado, start=1):
        total = dados["series"] + dados["derrotas_series"]
        winrate = (dados["series"] / total) * 100 if total > 0 else 0
        descricao.append(f"**#{i}** {dados['nome']} — 🏆 {dados['series']} séries — {winrate:.1f}% WR")

    embed = discord.Embed(
        title="🏆 Ranking de Vitórias em Séries",
        description="\n".join(descricao),
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

@bot.command()
async def rankingmapas(ctx):
    ranking = carregar_ranking()
    if not ranking:
        await ctx.send("⚠️ Nenhum dado de ranking encontrado.")
        return

    mapas_ordenado = sorted(ranking.items(), key=lambda x: x[1]["mapas"], reverse=True)
    descricao = []
    for i, (jogador_id, dados) in enumerate(mapas_ordenado, start=1):
        total = dados["mapas"] + dados["derrotas_mapas"]
        winrate = (dados["mapas"] / total) * 100 if total > 0 else 0
        descricao.append(f"**#{i}** {dados['nome']} — 🗺️ {dados['mapas']} mapas — {winrate:.1f}% WR")

    embed = discord.Embed(
        title="🗺️ Ranking de Vitórias em Mapas",
        description="\n".join(descricao),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command()
async def ranking_por_mapa(ctx, *, mapa_nome):
    ranking = carregar_ranking()
    if not ranking:
        await ctx.send("⚠️ Nenhum dado de ranking encontrado.")
        return

    mapa_nome = mapa_nome.title()
    if mapa_nome not in MAPAS:
        await ctx.send(f"❌ Mapa '{mapa_nome}' não encontrado.")
        return

    lista = []
    for jogador_id, dados in ranking.items():
        if mapa_nome in dados["por_mapa"]:
            vitorias = dados["por_mapa"][mapa_nome]["vitorias"]
            derrotas = dados["por_mapa"][mapa_nome]["derrotas"]
            total = vitorias + derrotas
            winrate = (vitorias / total) * 100 if total > 0 else 0
            lista.append((dados["nome"], vitorias, derrotas, winrate))

    if not lista:
        await ctx.send(f"⚠️ Nenhum dado para o mapa {mapa_nome}.")
        return

    lista.sort(key=lambda x: x[1], reverse=True)
    descricao = [f"**#{i+1}** {jogador} — 🗺️ {v} vitórias / {d} derrotas — {w:.1f}% WR"
                 for i, (jogador, v, d, w) in enumerate(lista)]

    embed = discord.Embed(
        title=f"🗺️ Ranking por Mapa: {mapa_nome}",
        description="\n".join(descricao),
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
async def rankingelo(ctx):
    ranking = carregar_ranking()
    if not ranking:
        await ctx.send("⚠️ Nenhum dado de ranking encontrado.")
        return

    elo_ordenado = sorted(ranking.items(), key=lambda x: x[1].get("elo", 1000), reverse=True)
    descricao = []

    for i, (jogador_id, dados) in enumerate(elo_ordenado, start=1):
        elo = dados.get("elo", 1000)
        descricao.append(f"**#{i}** {dados['nome']} — 🔰 Elo **{elo}**")

    embed = discord.Embed(
        title="🔰 Ranking de Elo",
        description="\n".join(descricao),
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
async def elo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    ranking = carregar_ranking()
    jogador_id = str(member.id)
    if jogador_id not in ranking:
        await ctx.send(f"❌ {member.display_name} não possui ranking.")
        return
    elo = ranking[jogador_id].get("elo", 1000)
    await ctx.send(f"🔰 Elo de {member.display_name}: **{elo}** pontos.")


@bot.command()
async def test_ranking(ctx): # Comando de teste para verificar se o ranking está atualizando e salvando
    atualizar_ranking("JogadorTeste", "Mirage", vencedor_serie=True)
    registrar_derrota("JogadorTeste", "Nuke", perdeu_serie=True)
    await ctx.send("Ranking de JogadorTeste atualizado para teste!")

@bot.command() # Sorteio de times
async def times(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        canal = ctx.author.voice.channel
        membros = canal.members

        if len(membros) < 2:
            await ctx.send("❌ Precisa de pelo menos 2 pessoas no canal de voz.")
            return

        membros_lista = membros[:]  # lista de Member

        random.shuffle(membros_lista)
        metade = len(membros_lista) // 2

        time1 = membros_lista[:metade]
        time2 = membros_lista[metade:]

        capitao1 = time1[0]
        capitao2 = time2[0]

        mensagem = (
            f"🎯 **Sorteio de Times** 🎯\n\n"
            f"🔵 **Time {time1[0].display_name}:**\n" + "\n".join(f"- {m.display_name}" for m in time1) + "\n\n"
            f"🟢 **Time {time2[0].display_name}:**\n" + "\n".join(f"- {m.display_name}" for m in time2)
        )

        await ctx.send(mensagem)

        bot.time1 = f"Time {time1[0].display_name}"
        bot.time2 = f"Time {time2[0].display_name}"
        bot.time1_membros = time1  # lista de Member
        bot.time2_membros = time2


    else:
        await ctx.send("❌ Você precisa estar em um canal de voz.")

@bot.command()
async def separar(ctx):
    if not hasattr(bot, 'time1') or not hasattr(bot, 'time2'):
        await ctx.send("⚠️ Você precisa sortear os times antes usando `.times`.")
        return

    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("❌ Você precisa estar conectado em uma call para eu criar as salas.")
        return

    canal_base = ctx.author.voice.channel
    categoria = canal_base.category

    if categoria is None:
        await ctx.send("⚠️ Não consegui identificar a categoria do seu canal de voz.")
        return

    call_time1 = await categoria.create_voice_channel(bot.time1)
    call_time2 = await categoria.create_voice_channel(bot.time2)

    await ctx.send(f"🔊 Salas criadas: **{bot.time1}** e **{bot.time2}**.")

    for membro in canal_base.members:
        if membro in bot.time1_membros:
            await membro.move_to(call_time1)
        elif membro in bot.time2_membros:
            await membro.move_to(call_time2)

    await ctx.send("✅ Jogadores movidos para suas respectivas calls.")

    async def monitorar_calls():
        while True:
            await asyncio.sleep(5)
            if len(call_time1.members) == 0 and len(call_time2.members) == 0:
                await call_time1.delete()
                await call_time2.delete()
                await ctx.send("🚫 As calls foram apagadas pois estão vazias.")
                break

    bot.loop.create_task(monitorar_calls())

async def escolher_pool_e_iniciar(ctx, modo):
    opções = "\n".join(f"- {nome}" for nome in POOLS_MAPAS.keys())
    await ctx.send(f"Escolha o pool de mapas para o modo {modo.upper()}:\n{opções}\nResponda com o nome do pool.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in POOLS_MAPAS

    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
        pool_nome = msg.content.lower()
        pool_mapas = POOLS_MAPAS[pool_nome]
    except asyncio.TimeoutError:
        await ctx.send("⏰ Tempo para escolher o pool acabou. Comando cancelado.")
        return

    # Aqui passou os parâmetros corretos
    try:
        ordem = ORDEM_PICKBAN_POR_POOL[pool_nome][modo]
    except KeyError:
        await ctx.send("❌ Ordem de pick/ban não definida para essa combinação de pool e modo.")
        return

    await pickban(ctx, modo, pool_mapas, ordem)



# Picks, bans, votação e backlog
def montar_ordem_pickban(modo, tamanho_pool, time1, time2):
    if modo == "md1":
        if tamanho_pool >= 3:
            return [("ban", time1), ("ban", time2)]
        else:
            return []  # Sem bans se tiver 2 mapas ou menos

    elif modo == "md3":
        ordem = [
            ("ban", time1), ("ban", time2), ("ban", time1), ("ban", time2),
            ("pick", time1), ("pick", time2)
        ]
        max_actions = min(len(ordem), tamanho_pool - 1)
        return ordem[:max_actions]

    elif modo == "md5":
        ordem = [
            ("ban", time1), ("ban", time2),
            ("pick", time1), ("pick", time2),
            ("ban", time1), ("ban", time2),
            ("pick", time1), ("pick", time2)
        ]
        max_actions = min(len(ordem), tamanho_pool - 1)
        return ordem[:max_actions]

    else:
        return []



async def pickban(ctx, modo, mapas_disponiveis, ordem):
    mapas_disponiveis = mapas_disponiveis.copy()
    picks = []
    resultados = []

    if not hasattr(bot, 'time1') or not hasattr(bot, 'time2'):
        await ctx.send("⚠️ Times não definidos. Use `.times` antes.")
        return

    tamanho_pool = len(mapas_disponiveis)

    if tamanho_pool < 2 and any(acao in ['ban', 'pick'] for acao, _ in ordem):
        await ctx.send("❌ Pool de mapas muito pequena para realizar bans/picks.")
        return

    max_vitorias = 1 if modo == "md1" else 2 if modo == "md3" else 3 if modo == "md5" else None

    if max_vitorias is None:
        await ctx.send("❌ Modo inválido.")
        return

    await ctx.send(f"🎯 **Iniciando picks e bans ({modo.upper()})!**")

    for i, (acao, time) in enumerate(ordem):
        nome_time = bot.time1 if time == "time1" else bot.time2
        descricao = ""
        emoji_mapa = {}

        for mapa in mapas_disponiveis:
            emoji = EMOJIS_MAPAS.get(mapa)
            if emoji:
                descricao += f"{str(emoji)} - {mapa}\n"
                emoji_mapa[str(emoji)] = mapa
            else:
                descricao += f"{mapa}\n"

        embed = discord.Embed(
            title=f"🗳️ Rodada {i + 1}: {acao.upper()} de {nome_time}",
            description=descricao,
            color=discord.Color.gold()
        )

        msg = await ctx.send(embed=embed)

        for emoji in emoji_mapa.keys():
            await msg.add_reaction(emoji)
            await asyncio.sleep(0.01)


        def check(reaction, user):
            return user != bot.user and reaction.message.id == msg.id and str(reaction.emoji) in emoji_mapa

        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            mapa_escolhido = emoji_mapa[str(reaction.emoji)]

            if mapa_escolhido not in mapas_disponiveis:
                await ctx.send("⚠️ Este mapa já foi banido ou escolhido, escolha outro.")
                continue
            else:
                if acao == "ban":
                    mapas_disponiveis.remove(mapa_escolhido)
                    await ctx.send(f"🗑️ **{mapa_escolhido} banido por {time}!**")
                elif acao == "pick":
                    mapas_disponiveis.remove(mapa_escolhido)
                    picks.append(mapa_escolhido)
                    await ctx.send(f"✅ **{mapa_escolhido} escolhido por {time}!**")


        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo esgotado.")
            return

    # Se sobrar 1 mapa e não houver picks, ele é o decisivo
    if len(mapas_disponiveis) == 0:
        await ctx.send("❌ Erro: todos os mapas foram banidos, sem mapas para jogar!")
        return
    elif len(mapas_disponiveis) == 1 and not picks:
        sobra = mapas_disponiveis[0]
        picks.append(sobra)
        await ctx.send(f"⚠️ O mapa **{sobra}** sobrou como decisivo!")


    await ctx.send("🏁 **Iniciando votação dos mapas!**")

    vit1 = 0
    vit2 = 0

    for mapa in picks:
        if (modo in ["md3", "md5"]) and (vit1 == max_vitorias or vit2 == max_vitorias):
            break

        emoji_mapa = EMOJIS_MAPAS.get(mapa)
        emoji_str = str(emoji_mapa) if emoji_mapa else ""

        embed = discord.Embed(
            title=f"🗺️ {emoji_str} **{mapa}**",
            description=f"📌 Quem venceu?\n\n🔵 {bot.time1}\n🟢 {bot.time2}",
            color=discord.Color.blue()
        )

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🔵")
        await msg.add_reaction("🟢")

        def check_voto(reaction, user):
            return user != bot.user and reaction.message.id == msg.id and str(reaction.emoji) in ["🔵", "🟢"]

        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=6000000.0, check=check_voto)
            vencedor = bot.time1 if str(reaction.emoji) == "🔵" else bot.time2
            perdedor = bot.time2 if vencedor == bot.time1 else bot.time1

            resultados.append({"mapa": mapa, "vencedor": vencedor})

            if vencedor == bot.time1:
                vit1 += 1
            else:
                vit2 += 1

            await ctx.send(f"🏆 **{vencedor} venceu no mapa {mapa}!**")
            await ctx.send(f"📊 Placar parcial: 🔵 {vit1} x {vit2} 🟢")

            # Envio no backlog
            backlog = bot.get_channel(BACKLOG_CHANNEL_ID)
            if backlog:
                embed_backlog = discord.Embed(
                    title=f"🗺️ Resultado do mapa {emoji_str} **{mapa}**",
                    description=f"🏆 Vencedor: **{vencedor}**\n\n"
                                f"🔵 **{bot.time1}**: {', '.join(m.display_name for m in bot.time1_membros)}\n"
                                f"🟢 **{bot.time2}**: {', '.join(m.display_name for m in bot.time2_membros)}",
                    color=discord.Color.purple()
                )
                embed_backlog.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/7/7a/Csgo-gun.png")
                await backlog.send(embed=embed_backlog)

        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo esgotado.")
            return

    campeao = bot.time1 if vit1 > vit2 else bot.time2 if vit2 > vit1 else None
    placar = f"{vit1}x{vit2}"

    if campeao:
        await ctx.send(f"🥇 **{campeao} venceu a série {placar}!**")

        for res in resultados:
            mapa = res["mapa"]
            vencedor = res["vencedor"]
            perdedor = bot.time1 if vencedor == bot.time2 else bot.time2

            for p in (bot.time1_membros if vencedor == bot.time1 else bot.time2_membros):
                atualizar_ranking(p, mapa)
                atualizar_elo_vitoria(p, mapas_ganhos=1)

            for p in (bot.time1_membros if perdedor == bot.time1 else bot.time2_membros):
                registrar_derrota(p, mapa)
                atualizar_elo_derrota(p, mapas_perdidos=1)

        for p in (bot.time1_membros if campeao == bot.time1 else bot.time2_membros):
            atualizar_ranking(p, mapa="", vencedor_serie=True)
            atualizar_elo_vitoria(p, series_ganhas=1)

        for p in (bot.time1_membros if campeao != bot.time1 else bot.time2_membros):
            registrar_derrota(p, mapa="", perdeu_serie=True)
            atualizar_elo_derrota(p, series_perdidas=1)

    else:
        await ctx.send(f"⚠️ Série empatada {placar} ou sem vencedor.")

    await publicar_ranking(ctx)



# 🏆 Ranking automático

async def publicar_ranking(ctx):
    ranking = carregar_ranking()
    ranking_channel = bot.get_channel(RANKING_CHANNEL_ID)

    if not ranking_channel:
        await ctx.send("⚠️ Canal de ranking não encontrado.")
        return

    # Apaga as mensagens antigas enviadas pelo bot no canal de ranking
    def is_bot_msg(m):
        return m.author == bot.user

    async for msg in ranking_channel.history(limit=50):
        if is_bot_msg(msg):
            try:
                await msg.delete()
            except:
                pass  # Pode falhar se a mensagem já foi deletada ou falta permissão

    # Depois, envia os embeds normalmente

    # Séries
    series_ordenado = sorted(ranking.items(), key=lambda x: x[1]["series"], reverse=True)
    series = []
    for i, (jogador, dados) in enumerate(series_ordenado, start=1):
        total = dados["series"] + dados["derrotas_series"]
        winrate = (dados["series"] / total) * 100 if total > 0 else 0
        series.append(f"**#{i}** {dados['nome']} — 🏆 {dados['series']} séries — {winrate:.1f}% WR")

    embed_series = discord.Embed(
        title="🏆 Ranking de Séries",
        description="\n".join(series) if series else "Sem dados.",
        color=discord.Color.gold()
    )
    await ranking_channel.send(embed=embed_series)

    # Mapas
    mapas_ordenado = sorted(ranking.items(), key=lambda x: x[1]["mapas"], reverse=True)
    mapas = []
    for i, (jogador, dados) in enumerate(mapas_ordenado, start=1):
        total = dados["mapas"] + dados["derrotas_mapas"]
        winrate = (dados["mapas"] / total) * 100 if total > 0 else 0
        mapas.append(f"**#{i}** {dados['nome']} — 🗺️ {dados['mapas']} mapas — {winrate:.1f}% WR")

    embed_mapas = discord.Embed(
        title="🗺️ Ranking de Mapas",
        description="\n".join(mapas) if mapas else "Sem dados.",
        color=discord.Color.blue()
    )
    await ranking_channel.send(embed=embed_mapas)


# 🎮 Comandos para iniciar pickban

@bot.command()
async def md1(ctx):
    await escolher_pool_e_iniciar(ctx, "md1")

@bot.command()
async def md3(ctx):
    await escolher_pool_e_iniciar(ctx, "md3")

@bot.command()
async def md5(ctx):
    await escolher_pool_e_iniciar(ctx, "md5")



bot.run('')
