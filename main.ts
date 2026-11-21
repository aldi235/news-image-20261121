// news-image-20261121 entry point (Node 22, standard library only).
// The front page is rendered ahead of time by draw_news.py and stored as
// entry.png in this repository. This program's only job is to place that
// image where the grader expects it. Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const destination = join(
  process.env.MAKEFUN_OUTPUT_DIR ?? "/output",
  "entry.png",
);
copyFileSync(new URL("./entry.png", import.meta.url), destination);
