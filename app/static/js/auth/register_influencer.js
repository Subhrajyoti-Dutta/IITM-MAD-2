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
                Username: this.username,
                Password: this.password,
                Full_Name: this.full_name,
                Country_Code: Number(this.country_code),
                Phone: Number(this.phone),
                Platform: {
                    Youtube: this.youtubeSelected,
                    Twitter: this.twitterSelected,
                    Instagram: this.instagramSelected,
                    Others: this.othersSelected,
                },
            };
            axios
                .post("/api/influencer_api/influencer", data)
                .then((response) => {
                    if (response.data.Influencer_ID != undefined) {
                        window.location.href = "/auth/login";
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
