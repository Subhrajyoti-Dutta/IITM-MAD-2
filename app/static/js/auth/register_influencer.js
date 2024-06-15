new Vue({
    el: "#app",
    data: {
        username: "",
        password: "",
        full_name: "",
        country_code: "",
        phone: "",
        youtubeSelected: false,
        twitterSelected: false,
        instagramSelected: false,
        othersSelected: false,
    },
    computed: {
        selectedPlatforms() {
            let platforms = [];
            if (this.youtubeSelected) platforms.push("youtube");
            if (this.twitterSelected) platforms.push("twitter");
            if (this.instagramSelected) platforms.push("instagram");
            if (this.othersSelected) platforms.push("others");
            return platforms.join(",");
        },
    },
    methods: {
        togglePlatform(platform) {
            if (platform === "youtube") {
                this.youtubeSelected = !this.youtubeSelected;
            } else if (platform === "twitter") {
                this.twitterSelected = !this.twitterSelected;
            } else if (platform === "instagram") {
                this.instagramSelected = !this.instagramSelected;
            } else if (platform === "others") {
                this.othersSelected = !this.othersSelected;
            }
        },
    },
});
