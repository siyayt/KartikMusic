#
# Copyright (C) 2025-present by TheAloneTeam@Github, < https://github.com/TheAloneTeam >.
#
# This file is part of < https://github.com/TheAloneTeam/KartikMusic > project,
# and is released under the "MIT License".
# Please see < https://github.com/TheAloneTeam/KartikMusic/blob/master/LICENSE >
#
# All rights reserved.
#

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends ffmpeg curl unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://deno.land/install.sh | sh


ENV DENO_INSTALL="/root/.deno"
ENV PATH="${DENO_INSTALL}/bin:${PATH}"

RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen

COPY . .

CMD ["bash", "start"]
