# Outreach kit

Everything here is for you to do yourself. Nothing gets posted or sent for you.
Portfolio: https://sejalborkar.vercel.app (the SEO work and the stats page are on the revamp preview until you OK the push to main).

What the site now does for search engines:
- Every page has its own title, description, canonical address, share image and `lang="en"` with an `x-default` language tag.
- `https://sejalborkar.vercel.app/sitemap.xml` lists every public page. `https://sejalborkar.vercel.app/robots.txt` lets every engine in and points to the sitemap.
- The home page tells search engines who you are (name, role, city, school, and links to LinkedIn, Behance, ArtStation, GitHub, Instagram and Webtoon). Each case study and art page is marked as your work.
- The ownership tags for Google, Bing, Yandex and Naver are read from Vercel environment variables, so verifying an engine never needs a code change.

Do sections 1 and 2 after revamp is merged to main. They verify the live address.

---

## 1. Google Search Console

1. Open https://search.google.com/search-console and sign in with your Google account.
2. Click the property selector (top left), then **Add property**.
3. Choose **URL prefix** and type `https://sejalborkar.vercel.app/` (with the `https://` and the slash at the end). Click **Continue**.
4. Under **Other verification methods**, open **HTML tag**. It shows a line like `<meta name="google-site-verification" content="abc123..." />`. Copy only the part inside `content="..."`.
5. Open https://vercel.com/sborkar2002s-projects/sejalborkar/settings/environment-variables
6. Click **Add New**. Key: `GOOGLE_SITE_VERIFICATION`. Value: the code you copied. Environments: tick **Production**. Click **Save**.
7. Open https://vercel.com/sborkar2002s-projects/sejalborkar/deployments, click the three dots on the newest Production deployment, then **Redeploy**. Wait until it says Ready.
8. Go back to the Search Console tab and click **Verify**.
9. In the left menu, open **Sitemaps**. Under "Add a new sitemap", type `sitemap.xml` and click **Submit**.
10. Optional: open **URL inspection**, paste `https://sejalborkar.vercel.app/` and click **Request indexing**. Repeat for 2 or 3 case studies.

Google treats the sitemap as a hint, so new pages can take days to weeks to show up.

## 2. Bing Webmaster Tools (also feeds DuckDuckGo)

DuckDuckGo says most of its links come from Bing, so this one step covers both.

1. Open https://www.bing.com/webmasters and sign in (a Microsoft, Google or Facebook account works).
2. On the welcome screen choose **Import your sites from GSC** and click **Import**.
3. Sign in with the same Google account and allow access. Tick `https://sejalborkar.vercel.app/` and click **Import**.
4. Bing verifies it automatically and picks up the sitemap from Search Console. Keep the Google access in place, because Bing re-syncs from it.

If the import is not offered: choose **Add your site manually**, pick the **HTML Meta Tag** option, copy the code inside `content="..."`, and add it in Vercel as `BING_SITE_VERIFICATION` (same steps as section 1, steps 5 to 8). Then submit `https://sejalborkar.vercel.app/sitemap.xml` under **Sitemaps**.

## 3. Optional engines

- **Yandex** (Russia, Turkey): https://webmaster.yandex.com. Add the site, choose the meta tag method, and save the code in Vercel as `YANDEX_VERIFICATION`. Yandex indexes English sites, but it favours Russian-language results, so expect little from it.
- **Naver** (South Korea): https://searchadvisor.naver.com. Its verification tag name is `naver-site-verification`. Save the code as `NAVER_SITE_VERIFICATION`. The interface is mostly Korean, and I could not confirm that Naver lists English-only sites well. Skip it unless you target Korean clients.

Redeploy after adding any of these (section 1, step 7).

## 4. What is and is not realistic

**China.** Google Search has been blocked in mainland China since 2010. Baidu ranks sites hosted inside China, ideally with an ICP licence, much better than foreign ones, and an English-only site on foreign hosting will do poorly there. Vercel's own guide says it has no servers in mainland China, that speed there can be poor, and that `*.vercel.app` addresses may be blocked or throttled. A custom domain helps a little. Reaching readers in China would need a mainland host and a Chinese version of the site, which is out of scope for now. People in China who use a VPN can still reach the site.

**Japanese or Chinese meta descriptions.** Not worth adding on their own. Google picks the page's language from the visible text and usually writes the snippet from the page itself, so a Japanese description over an English page would most likely be ignored or look mismatched. The right way is a real translated page at its own address (for example `/ja/`) with language tags. Worth doing later for Japan if Japanese clients start showing up in the stats.

**Everywhere else** (US, UK, Europe, Japan, Korea, Russia): standard metadata, a sitemap and fast pages are what Google, Bing, Yandex and Naver all read. That part is done.

## 5. Your private analytics page

Open it from the **ANALYTICS** link at the very bottom of the site, or go straight to https://sejalborkar.vercel.app/analytics. It shows visitors and page views over 30 days, top pages, countries, how people found the site, phone or computer, a daily speed test, and the last full site checkup with charts. Anyone can see the sign-in box, but only your email and password open it, and search engines are told to stay out.

Add these in Vercel (https://vercel.com/sborkar2002s-projects/sejalborkar/settings/environment-variables). Click **Add New** for each, tick **Production** and **Preview**, and click **Save**:

1. `ANALYTICS_EMAIL`: what you will type in the Email box. You chose `Sejal Borkar`. Capitals and outer spaces do not matter.
2. `ANALYTICS_PASSWORD`: what you will type in the Password box. You chose `Sejal Borkar`. This one must match exactly.
   Your name is on every page of the site, so anyone who guesses it can open your stats. The stats are not dangerous, but if you want them truly private, use a password that is not your name. You can change it here any time; changing it signs out every browser.
3. `VERCEL_ANALYTICS_TOKEN`:
   1. Open https://vercel.com/account/settings/tokens
   2. Click **Create Token**. Name it `portfolio stats`. Scope: your personal account (sborkar2002s-projects). Expiration: pick 1 year, and set a reminder to renew it.
   3. Click **Create**, copy the token once, and paste it straight into the Vercel variable. Do not paste it anywhere else, including chat.
4. `VERCEL_ANALYTICS_PROJECT_ID`: open https://vercel.com/sborkar2002s-projects/sejalborkar/settings, scroll to **Project ID** and copy it (it starts with `prj_`).
5. `PAGESPEED_API_KEY`: needed for the speed section. Google refuses speed tests that come without a key. To get a free key:
   1. Open https://console.cloud.google.com/apis/library/pagespeedonline.googleapis.com and click **Enable** (create a project if asked; this API is free).
   2. Open https://console.cloud.google.com/apis/credentials, click **Create credentials**, then **API key**, and copy it into the Vercel variable.
6. Redeploy: open https://vercel.com/sborkar2002s-projects/sejalborkar/deployments, click the three dots on the newest Production deployment, then **Redeploy**. Wait until it says Ready.
7. Open https://sejalborkar.vercel.app/analytics and sign in. You stay signed in for 14 days on that browser.

Until steps 1 and 2 are done, the page says sign-in is not switched on and shows nothing.

If the page says Vercel did not let the token read the visits: Vercel documents the analytics API, but I could not confirm that it is open on the free Hobby plan. In that case the Vercel dashboard (https://vercel.com/sborkar2002s-projects/sejalborkar/analytics) still has every number, and the page's speed section keeps working. Vercel's own Speed Insights score has no API at all, so it stays in the dashboard.

---

## 6. Where to post your work (free)

| Where | For | Notes |
|---|---|---|
| Behance (https://www.behance.net) | Case studies, comics | The biggest creative hiring audience. Sourced is already there. |
| Dribbble (https://dribbble.com) | Single UI shots | Free account. Pro is paid and not needed. |
| ArtStation (https://www.artstation.com/jen_chan) | Illustration | Already yours. Add the comic pages as a project. |
| LinkedIn Featured section | Everything | Pin the portfolio link and one case study to your profile. |
| foriio (https://www.foriio.com) | Japan | Japanese portfolio site, free plan (Pro is about 980 yen a month). |
| pixiv (https://www.pixiv.net) | Japan, illustration and comics | Free, English interface. Best for the comic and illustration side. |
| Skeb (https://skeb.jp) | Japan, commissions | Not a portfolio but a route to paid Japanese commissions. Has English support. |
| WEBTOON Canvas | Comics | One Last Chance is already there. A new episode keeps the profile alive. |

Paid, so left out: Awwwards (about 65 USD per site). Read.cv shut down in 2025.

## 7. Behance and Dribbble plan

One post a week for six weeks, so the profiles stay active without a big push.

| Week | Behance | Dribbble |
|---|---|---|
| 1 | Marketing site and 20-component library | The maturity chart with its level stepper |
| 2 | Lead-gen assessment (the five result states) | The result screen before and after |
| 3 | AppsForBharat blog and its thumbnail system | The category thumbnails as a grid |
| 4 | Video production system (storyboard frames and the build loop) | One storyboard frame |
| 5 | Comics: One Last Chance panels, Pocket Toons pages, The Last Over (say how AI was used on each, as the site does) | One comic panel |
| 6 | #futureofhr (only once you are happy to publish the take-home) | The "you are on mute" hero |

Every post links back to the matching page on the portfolio. Use real tags people search for: `product design`, `UX case study`, `B2B SaaS`, `design system`, `webtoon`, `comic art`.

Check before publishing: take-homes (#futureofhr, The Last Over) only after that hiring process is closed, unless you decide otherwise. Keep the Tetriz launch film to the three excerpts already on the site.

---

## 8. LinkedIn posts (ready to post)

**Post 1: the portfolio**

> I rebuilt my portfolio.
>
> It has six case studies, from research to merged pull requests: a marketing site built from a 20-component kit, a lead-gen assessment I redesigned and shipped in 3 pull requests, a company blog that is live today, and the system behind a 2:23 product launch film.
>
> It also has the other half of me: comics, illustration and motion work, because I have been drawing since 2020.
>
> And there is a small pixel cat who follows you around. You can dress it up.
>
> sejalborkar.vercel.app

**Post 2: the comic videos**

> One of the comic videos I made to explain AI engineering ideas passed 30,000 organic views on Instagram.
>
> Each episode starts as a script, then a rough voice pass before any art, to hear whether the joke lands. Panels are laid out in Figma, characters generated and keyed onto clean backgrounds, voices from ElevenLabs, and everything animated in Remotion with word-by-word captions.
>
> The whole series and how it was made: sejalborkar.vercel.app/art/motion

**Post 3: Sourced**

> As an artist, I watched the feeds I loved fill up with AI images. So I designed Sourced, an app where human-made and AI art sit in separate feeds and artists can show the process behind a post.
>
> I surveyed 25+ artists first. 92.9% wanted AI art verified, and 82.1% said a buddy would push them to keep making work, so artists are paired as Art Buddies with a shared streak.
>
> The full case study, with the clickable prototype: sejalborkar.vercel.app/work/sourced

---

## 9. Cold message for clients abroad

Short enough for a LinkedIn note, an email or a Behance message. Fill in the brackets.

> Hi [name],
>
> I am Sejal, a product designer in Bengaluru who also draws comics and illustration. I saw [their product or recent launch] and [one specific thing you noticed].
>
> I design B2B SaaS from research to shipped code. Recent work: feature pages built from a 20-component kit, a lead-gen assessment I redesigned and shipped, and a product launch film made in Remotion. Portfolio: sejalborkar.vercel.app
>
> If you need help with [the specific thing], I would be glad to talk.
>
> Sejal

Keep each message specific to that company. One real detail about their product does more than a long list of skills.
