<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# sonarr, radarr, what more software is there ending in arr?

The "Arr" suite (often called the \*arr stack) has expanded well beyond just Sonarr and Radarr. These tools are generally designed for media automation, management, and grabbing content via Usenet or BitTorrent.

### Core Media Managers

These are the primary applications for managing specific types of media libraries.

| Application  | Purpose                                                                                                                                                  |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Lidarr**   | Music collection manager for automating artist and album downloads [^1_3][^1_10].                                                                        |
| **Readarr**  | eBook and audiobook manager for authors and book series [^1_5][^1_10].                                                                                   |
| **Prowlarr** | Indexer manager/proxy. It integrates with the other apps to manage torrent/Usenet indexers in one place (replaces Jackett for many users) [^1_3][^1_12]. |
| **Bazarr**   | Companion app that manages and downloads subtitles for Sonarr and Radarr media [^1_3][^1_6].                                                             |
| **Whisparr** | Adult video collection manager (NSFW) [^1_6][^1_10].                                                                                                     |

### Utilities \& Integrations

These tools enhance the core stack, often bridging gaps or adding specific functionality.

- **Overseerr / Jellyseerr**: While they don't end in "arr", these are the standard request management front-ends for the stack (Overseerr for Plex, Jellyseerr for Jellyfin).[^1_2]
- **Recyclarr**: Automatically syncs TRaSH guides (optimal quality profiles/custom formats) to Sonarr/Radarr instances.[^1_3][^1_7]
- **Unpackerr**: Extracts compressed archives after download so the \*arr apps can import them.[^1_6][^1_7]
- **Homarr**: A dashboard to organize all these services (and others) into a single homepage.[^1_4]
- **Crossarr / Cross-Seed**: Tools for cross-seeding torrents across multiple trackers.[^1_3]
- **Flaresolverr**: A proxy server to bypass Cloudflare protection on indexers.[^1_3]
- **Tdarr**: Distributed transcoding automation (uses FFmpeg/HandBrake) to standardize your library's codecs and containers.[^1_3]

### Less Common / Niche Tools

- **Mylar3**: Automated comic book downloader (functionally an "\*arr" for comics, though named differently).[^1_12]
- **LazyLibrarian**: An alternative to Readarr for books.[^1_5]
- **Bonarr**: A fork of Radarr specifically for adult content (older, largely superseded by Whisparr).[^1_5]
- **Notifiarr**: A unified notification system for the entire stack, providing detailed alerts and stats.
  <span style="display:none">[^1_1][^1_11][^1_13][^1_14][^1_15][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://www.reddit.com/r/selfhosted/comments/1r91wan/suggestion_for_simpler_software_than_arr_radarr/

[^1_2]: https://www.facebook.com/groups/homeserversetups/posts/3159871540981002/

[^1_3]: https://github.com/Ravencentric/awesome-arr

[^1_4]: https://homarr.dev

[^1_5]: https://www.reddit.com/r/sonarr/comments/jo0h38/i_know_about_sonarr_radarr_and_ive_just_learnt/

[^1_6]: https://github.com/OliTechFR/Discovarr/

[^1_7]: https://github.com/OliTechFR/Discovarr

[^1_8]: https://ravencentric.cc/awesome-arr/

[^1_9]: https://github.com/autobrr/community-feedback/discussions/2

[^1_10]: https://github.com/hxck/arrsuite

[^1_11]: https://www.reddit.com/r/sonarr/comments/1fw2qq3/all_the_arr_applications/

[^1_12]: https://www.reddit.com/r/Piracy/comments/tlktya/arr_software_suite/

[^1_13]: https://www.reddit.com/r/radarr/comments/17xs5qc/is_there_an_app_like_radarr_but_for_files/

[^1_14]: https://www.reddit.com/r/selfhosted/comments/jmq4y9/list_of_all_of_the_arr_software/

[^1_15]: https://www.reddit.com/r/radarr/comments/1e7a642/is_there_more/

---

# give me the links for each one of the packages you've mentioned. ideally github but if they only have a homepage that's fine too.

Here are the links for the software mentioned, categorized by their function within the stack.

### Core Media Managers

These are the standard "Starr" apps for managing your libraries.

| Application  | GitHub Repository                                               | Homepage / Documentation                 |
| :----------- | :-------------------------------------------------------------- | :--------------------------------------- |
| **Sonarr**   | [Sonarr/Sonarr](https://github.com/Sonarr/Sonarr)               | [sonarr.tv](https://sonarr.tv)           |
| **Radarr**   | [Radarr/Radarr](https://github.com/Radarr/Radarr)               | [radarr.video](https://radarr.video)     |
| **Lidarr**   | [Lidarr/Lidarr](https://github.com/Lidarr/Lidarr)               | [lidarr.audio](https://lidarr.audio)     |
| **Readarr**  | [Readarr/Readarr](https://github.com/Readarr/Readarr)           | [readarr.com](https://readarr.com)       |
| **Prowlarr** | [Prowlarr/Prowlarr](https://github.com/Prowlarr/Prowlarr)       | [prowlarr.com](https://prowlarr.com)     |
| **Bazarr**   | [morpheus65535/bazarr](https://github.com/morpheus65535/bazarr) | [bazarr.media](https://www.bazarr.media) |
| **Whisparr** | [Whisparr/Whisparr](https://github.com/Whisparr/Whisparr)       | [whisparr.com](https://whisparr.com)     |

### Utilities \& Integrations

Tools that handle requests, notifications, and post-processing.

| Application      | GitHub Repository                                                         | Homepage / Documentation                           |
| :--------------- | :------------------------------------------------------------------------ | :------------------------------------------------- |
| **Overseerr**    | [sct/overseerr](https://github.com/sct/overseerr)                         | [overseerr.dev](https://overseerr.dev)             |
| **Jellyseerr**   | [Fallenbagel/jellyseerr](https://github.com/Fallenbagel/jellyseerr)       | [docs.jellyseerr.dev](https://docs.jellyseerr.dev) |
| **Recyclarr**    | [recyclarr/recyclarr](https://github.com/recyclarr/recyclarr)             | [recyclarr.dev](https://recyclarr.dev)             |
| **Unpackerr**    | [Unpackerr/unpackerr](https://github.com/Unpackerr/unpackerr)             | [unpackerr.zip](https://unpackerr.zip)             |
| **Notifiarr**    | [Notifiarr/notifiarr](https://github.com/Notifiarr/notifiarr)             | [notifiarr.com](https://notifiarr.com)             |
| **Flaresolverr** | [FlareSolverr/FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) | —                                                  |
| **Cross-Seed**   | [cross-seed/cross-seed](https://github.com/cross-seed/cross-seed)         | [cross-seed.org](https://cross-seed.org)           |
| **Homarr**       | [homarr-labs/homarr](https://github.com/homarr-labs/homarr)               | [homarr.dev](https://homarr.dev)                   |
| **Tdarr**        | [HaveAGitGat/Tdarr](https://github.com/HaveAGitGat/Tdarr)                 | [tdarr.io](https://tdarr.io)                       |

### Niche \& Alternatives

Specialized tools or alternatives to the main stack.

| Application       | Repository                                                                    | Notes                                                                          |
| :---------------- | :---------------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| **Mylar3**        | [mylar3/mylar3](https://github.com/mylar3/mylar3)                             | The active fork of Mylar for comic books.                                      |
| **LazyLibrarian** | [LazyLibrarian/LazyLibrarian](https://gitlab.com/LazyLibrarian/LazyLibrarian) | Hosted on GitLab, not GitHub.                                                  |
| **Bonarr**        | —                                                                             | Mostly abandoned; **Whisparr** is the recommended successor for adult content. |

<span style="display:none">[^2_1][^2_10][^2_11][^2_12][^2_13][^2_14][^2_15][^2_16][^2_17][^2_18][^2_19][^2_2][^2_20][^2_21][^2_22][^2_23][^2_24][^2_25][^2_26][^2_27][^2_28][^2_29][^2_3][^2_30][^2_4][^2_5][^2_6][^2_7][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: https://github.com/Ravencentric/awesome-arr

[^2_2]: https://github.com/Servarr/Wiki

[^2_3]: https://github.com/plexguide/Huntarr.io

[^2_4]: https://github.com/OliTechFR/Discovarr

[^2_5]: https://github.com/Ravencentric/awesome-arr/blob/main/README.md

[^2_6]: https://www.reddit.com/r/JellyfinCommunity/comments/1r5a1bw/seerr_v300_released_unified_successor_to/

[^2_7]: https://github.com/Notifiarr/notifiarr

[^2_8]: https://github.com/hxck/arrsuite

[^2_9]: https://github.com/homarr-labs/homarr/issues/1047

[^2_10]: https://www.youtube.com/watch?v=oaQD-d2kg-I

[^2_11]: https://wiki.servarr.com

[^2_12]: https://github.com/Fallenbagel/jellyseerr

[^2_13]: https://github.com/saltyorg/Sandbox/blob/master/sandbox.yml

[^2_14]: https://www.reddit.com/r/selfhosted/comments/1facgzf/which_other_apps_can_make_rr_apps_better/

[^2_15]: https://github.com/timotheeandres/jellyseerr

[^2_16]: https://github.com/Unpackerr/unpackerr

[^2_17]: https://github.com/MichaIng/DietPi/issues/7135

[^2_18]: https://github.com/orgs/Unpackerr/packages/container/package/unpackerr

[^2_19]: https://github.com/hotio/unpackerr

[^2_20]: https://github.com/Unpackerr

[^2_21]: https://hub.docker.com/r/recyclarr/recyclarr

[^2_22]: https://cross-seed.org

[^2_23]: https://github.com/mylar3/mylar3

[^2_24]: https://lazylibrarian.gitlab.io

[^2_25]: https://github.com/Unpackerr/xt

[^2_26]: https://trash-guides.info/Recyclarr/

[^2_27]: https://www.cross-seed.org

[^2_28]: https://mylarcomics.com/docs/installation/source

[^2_29]: https://libreselfhosted.com/project/lazylibrarian/

[^2_30]: https://drfrankenstein.co.uk/unpackerr-in-container-manager-on-a-synology-nas/
