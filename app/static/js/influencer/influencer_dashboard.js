new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        averageRating: 0,
        totalEarnings: 0,
        loading: true,
        activeCampaigns: [],
        newCampaigns: [],
    },
    methods: {
        fetchData() {
            axios
                .get("/api/influencer_api/influencer/1947380509")
                .then((response) => {
                    this.id = response.data["ID"];
                    this.username = response.data["Username"];
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                    this.loading = false;
                });
        },
        fetchAds(status) {
            return axios
                .get(
                    `/api/influencer_api/influencer/1947380509/campaign/${status}`
                )
                .then((response) => {
                    console.log(response.data);
                    return response.data;
                })
                .catch((error) => {
                    console.error(`Error fetching ${status} ads:`, error);
                    return [];
                });
        },
        viewCampaign(campaignId) {
            window.location.href = `/campaign/${campaignId}`; // Replace with actual URL structure
        },
        acceptCampaign(campaignId, adRequestID) {
            axios
                .put(
                    `/api/campaign_api/campaign/${campaignId}/adrequest/${adRequestID}`,
                    {
                        status: "active",
                    }
                ) // Replace with actual endpoint
                .then((response) => {
                    console.log("Campaign accepted:", response);
                    this.fetchAds("NULL").then((data) => {
                        this.newCampaigns = data;
                    });
                    this.fetchAds("active").then((data) => {
                        this.activeCampaigns = data;
                    });
                })
                .catch((error) => {
                    console.error("Error accepting campaign:", error);
                });
        },
        rejectCampaign(campaignId) {
            axios
                .post(`/api/influencer_api/campaign/${campaignId}/reject`) // Replace with actual endpoint
                .then((response) => {
                    console.log("Campaign rejected:", response);
                    this.fetchAds("NULL").then((data) => {
                        this.newCampaigns = data;
                    });
                })
                .catch((error) => {
                    console.error("Error rejecting campaign:", error);
                });
        },
    },
    created() {
        this.fetchData();
        this.fetchAds("active").then((data) => {
            this.activeCampaigns = data;
        });
        this.fetchAds("NULL").then((data) => {
            this.newCampaigns = data;
        });
    },
});
