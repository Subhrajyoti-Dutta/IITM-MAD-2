new Vue({
    el: "#app",
    data: {
        username: "",
        password: "",
        full_name: "",
        country_code: 0,
        phone: 0,
        youtubeSelected: false,
        twitterSelected: false,
        instagramSelected: false,
        othersSelected: false,
        error: "",
    },
    methods: {
        register() {
            const data = {
                username: this.username,
                password: this.password,
                full_name: this.full_name,
                country_code: Number(this.country_code),
                phone: Number(this.phone),
                youtube: this.youtubeSelected,
                twitter: this.twitterSelected,
                instagram: this.instagramSelected,
                others: this.othersSelected,
            };
            axios
                .post("/auth/register_influencer", data)
                .then((response) => {
                    if (response.data.success) {
                        window.location.href = response.data.next;
                    } else {
                        this.error = response.data.message;
                    }
                })
                .catch((error) => {
                    this.error = "An error occurred during registration.";
                });
        },
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
