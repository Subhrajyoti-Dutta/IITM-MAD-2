new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        influencerData: {},
        editValues: {},
        editMode: false,
        loading: true,
        presence: {},
    },
    computed: {
        averageRating() {
            if (!this.influencerData.campaigns) return 0;
            const totalRating = this.influencerData.campaigns.reduce(
                (acc, campaign) => acc + campaign.rating,
                0
            );
            return (totalRating / this.influencerData.campaigns.length).toFixed(
                2
            );
        },
        totalEarnings() {
            if (!this.influencerData.campaigns) return 0;
            return this.influencerData.campaigns.reduce(
                (acc, campaign) => acc + campaign.earnings,
                0
            );
        },
    },
    methods: {
        enableEdit() {
            this.editValues = { ...this.influencerData };
            this.editMode = true;
        },
        saveChanges() {
            this.influencerData = { ...this.editValues };
            this.editMode = false;
            axios
                .put(
                    "/influencer_api/influencer/1947380509",
                    this.influencerData
                )
                .then((response) => {
                    console.log("Data updated successfully");
                })
                .catch((error) => {
                    console.error("Error updating data:", error);
                });
        },
        cancelEdit() {
            this.editMode = false;
            this.editValues = {};
        },
        togglePlatform(platform) {
            this.editValues["Platform"][platform] =
                !this.editValues["Platform"][platform];
        },
    },

    created() {
        console.log("Vue instance is created");
        axios
            .get("/influencer_api/influencer/1947380509")
            .then((response) => {
                this.id = response.data["ID"];
                delete response.data["ID"];
                this.presence = response.data["Platform Presence"];
                delete response.data["Platform Presence"];
                this.influencerData = response.data;
                this.loading = false;
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                this.loading = false;
            });
    },
});