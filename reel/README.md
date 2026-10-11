# మాట్లాడే మొబైల్ — Object Talk Telugu Reel (30s, 9:16)

A production pack for a 30-second Pixar-style Telugu awareness reel about screen addiction.
It is built to match the two reference images in `references/`, so both characters look the same in every clip.

| File | Use |
|---|---|
| `references/boy-bedroom.webp` | Boy and bedroom reference. Use it as the start frame or image reference. |
| `references/phone-character-sheet.webp` | Phone character turnaround and expressions. Use it as the character reference. |
| `subtitles_te_en.srt` | Telugu dialogue with English subtitles, timed to the 30s cut. |

---

## Why the reel is split into 4 clips

Current video models (Veo 3, Seedance, Gen-4.5, Kling) render **8–10 seconds per generation**.
If you ask for one 30-second shot, you get character drift and dialogue that doesn't line up.
Generate the 4 clips below with the **same character block pasted into each one**, then join them in an editor (CapCut, Descript, or Premiere).

**Telugu lip-sync:** most models do Telugu speech and lip-sync poorly. Two ways to get it right:
1. **Best quality:** record or generate the Telugu voice lines first (a voice actor or Telugu TTS), then lip-sync them onto the clips with a lip-sync tool.
2. **One step:** use a model with native audio (for example Veo 3) and put the Telugu line in quotes. Check the pronunciation, and regenerate any clip that sounds wrong.

---

## Character block (paste at the top of EVERY clip prompt)

```
CHARACTER LOCK — keep identical in every shot:
PHONE "MOBI": a glossy black modern smartphone with a thin gold/bronze metal frame and a top notch.
Big round cartoon eyes with teal-green irises and white highlights, thick expressive black eyebrows,
a wide expressive mouth with pink tongue — all drawn on the black screen. Thin black rubber-hose
arms ending in white four-finger cartoon gloves; thin black legs with chunky white sneakers.
Back side shows a dual camera. Funny, warm, slightly bossy, ultimately caring.

BOY "CHINTU": Indian teenage boy, about 14, slim, medium-brown skin, messy spiky black hair,
thick eyebrows, tired droopy eyes with faint dark circles. Navy-blue pajama set with tiny white
star print, barefoot. Owns a small brown teddy bear.

BEDROOM: cozy teenage bedroom at night. Wooden single bed with a colorful patchwork quilt and
grey pillows; wooden bedside table with a warm glowing lamp, a glass of water, a silver twin-bell
alarm clock and stacked books; wall shelves with books and toys; movie posters; a desk with a
laptop; a window with sheer white curtains letting in cool blue moonlight; a chair with a blanket.

STYLE: Pixar-style 3D animation, cinematic lighting (warm lamp key light + cool blue moonlight
rim + phone-screen glow on faces), shallow depth of field, soft film grain, vertical 9:16,
family friendly. No text, no subtitles, no watermark, no extra fingers, no face distortion,
no design changes between shots.
```

---

## Clip 1 — 0:00–0:08 · Midnight scroll → phone wakes up

**References:** `boy-bedroom.webp` as start frame + `phone-character-sheet.webp`

```
[CHARACTER LOCK]

0–4s: Close-up of the alarm clock on the bedside table, both hands pointing straight up at
12:00, ticking. Rack focus to Chintu lying sideways on the bed under the patchwork quilt,
face lit blue by his phone, giggling at short videos. Insert shot: his thumb flicking
up the screen again and again. He yawns hugely but keeps scrolling. Soft notification pings.

4–8s: Sudden "boing!" — the phone in his hand sprouts cartoon eyes, eyebrows, mouth,
arms and legs (exactly as in the character sheet), springs out of his hand and lands
upright on the quilt. It plants gloved hands on its hips, eyebrows angry, then points
sharply at the clock. Fast camera push-in to the phone's angry face as it speaks.

Dialogue (PHONE, loud, comic-angry Telugu, clear lip-sync):
"ఒరేయ్ బాబూ! టైమ్ ఎంతైందో తెలుసా? అర్ధరాత్రి పన్నెండు!"

Audio: clock ticking, phone notification pings, cartoon "boing" spring sound, light
playful pizzicato music that stops abruptly on the phone's line.
```

## Clip 2 — 0:08–0:15 · "ఇంకో ఐదు నిమిషాలే!"

```
[CHARACTER LOCK]

Medium two-shot on the bed. Chintu barely glances up, sleepy half-lidded eyes, lazy smile,
holds up five fingers toward the phone, his other thumb still swiping in the air out of habit
as if scrolling. He says his line.

Dialogue (BOY, lazy, sleepy Telugu, clear lip-sync):
"ఇంకో ఐదు నిమిషాలే రా!"

Beat of silence. The phone gives a big dramatic facepalm with its white glove, slowly
drags the glove down its screen-face, shakes its head, then turns and stares straight
into the camera with a deadpan "can you believe this guy?" look.

Audio: comic pause, a single "wah-wah" trombone sting on the camera look.
```

## Clip 3 — 0:15–0:23 · "చార్జ్ నాకు… డిశ్చార్జ్ నీకు!"

```
[CHARACTER LOCK]

The phone steps closer, points a gloved finger at Chintu's tired, red-rimmed eyes, then at
the alarm clock. Its face softens from anger into real concern — eyebrows tilt up, eyes go glossy.

Quick 3-shot montage (each ~1s, same bedroom, same pajamas, warm-blue palette):
  a) Chintu's head nodding off, jerking awake, still holding the screen.
  b) A school book lying untouched and closed on the desk, gathering dust.
  c) An incoming video call from a friend ringing and going "missed" while he keeps scrolling.
Return to a tight close-up of the phone's worried face for the end of the line.

Dialogue (PHONE, emotional, sincere Telugu, clear lip-sync):
"నీ ఐదు నిమిషాలు గంటలవుతున్నాయ్! నన్ను ఛార్జింగ్ పెడుతున్నావ్… నీ ఆరోగ్యాన్ని డిశ్చార్జ్ చేస్తున్నావ్!"

Audio: music drops to a soft piano and strings, a slow heartbeat-like low pulse under the montage.
```

## Clip 4 — 0:23–0:30 · Realisation → sleep → end card

```
[CHARACTER LOCK]

0–4s: Chintu stops scrolling. He looks at the phone, then at the clock, and his smile fades
as he understands. He gently switches off the screen, places the phone on the bedside table
next to the lamp, stretches, hugs his teddy bear and lies down. The phone's angry face melts
into a warm, proud smile and it says softly:

Dialogue (PHONE, soft, warm Telugu, clear lip-sync):
"నన్ను వాడు రా… కానీ నీ జీవితం మొత్తం నాతోనే గడపకు!"

4–7s: Chintu sleeps peacefully, hugging the teddy. The phone sits quietly on the bedside table,
gives one tiny wink and its face dims to black. The lamp clicks off; only soft blue moonlight
remains. Slow cinematic camera pull-back through the room toward the window.
Leave clean empty space in the upper third of the frame for the end-card text (added in editing).

Audio: lamp click, gentle crickets outside, warm hopeful music swell to the end.
```

---

## End card (add in the editor, not in the generator)

Generators garble Telugu script, so add the end card as text in your editor over the last 3 seconds:

> **ఫోన్ నీ చేతిలో ఉండాలి… నీ జీవితం ఫోన్ చేతిలో కాదు!**
> *Keep the phone in your hand, not your life in the phone's hand.*

Suggested font: **Noto Sans Telugu Bold** (or Ramabhadra / Mandali) in white with a soft dark shadow, centred in the top third.

---

## Timing and voice direction

| Time | Clip | Action | Emotion / voice |
|---|---|---|---|
| 0:00–0:04 | 1 | Boy scrolling at midnight | Funny, relatable |
| 0:04–0:08 | 1 | Phone wakes up and scolds him | Loud, comic-angry |
| 0:08–0:15 | 2 | "Five more minutes" + facepalm | Lazy, sleepy / comic deadpan |
| 0:15–0:23 | 3 | Phone explains the cost | Sincere, emotional |
| 0:23–0:27 | 4 | Boy puts the phone away | Realisation, soft and warm |
| 0:27–0:30 | 4 | Sleep + end card | Calm, hopeful |

**Voices:** Phone: a bright, slightly nasal comic voice (think a Telugu cartoon dub), playful "ఒరేయ్" energy that turns tender in clips 3–4. Boy: a young teen voice, drowsy, words slurred with a yawn.

---

## Changes from the original prompt

- **Phone design now matches the character sheet.** The arms are black with white gloves, it has black legs with white sneakers and teal eyes. The original said "white cartoon arms", which would cause drift.
- **The clock matches the reference.** The original said "digital clock", but the bedroom image has an analog twin-bell alarm clock, so both hands point at 12.
- **Teddy bear and star pajamas are kept** from the bedroom reference, and the teddy is used in the ending.
- **Split into 4 clips of 7–8s each** so every shot stays inside what video models can generate.
- **Scene 1 dialogue is shortened** to "…అర్ధరాత్రి పన్నెండు!" so it fits a 4-second window.
- **The last line is clearer**: "నీ జీవితం మొత్తం నాతోనే గడపకు" ("don't spend your *whole* life with me").
- **The end card is added in editing**, because AI generators render Telugu text badly.

---

## Caption and hashtags for posting

```
ఐదు నిమిషాలే అనుకుంటాం… కానీ? 📱😴
Tag that friend who says "just 5 more minutes" every night! 👇

#ObjectTalk #TeluguReels #MobileAddiction #ScreenTime #TeluguShorts
#DigitalDetox #Telugu #AwarenessVideo #PixarStyle #AIAnimation
```
