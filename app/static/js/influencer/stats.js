new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        averageRating: 0,
        totalEarnings: 0,
        loading: true,
        totalCampaigns: 0,
        activeCampaigns: 0,
        completedCampaigns: 0,
        rejectedCampaigns: 0,
        totalReach: 0,
        totalPosts: 0,
        totalLikes: 0,
        campaigns: [],
    },
    methods: {
        fetchData() {
            axios
                .get(`/api/influencer_api/influencer/${this.id}`)
                .then((response) => {
                    this.username = response.data["Username"];
                    this.averageRating = response.data["Rating"];
                    this.totalEarnings = response.data["Earnings"];
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                    this.loading = false;
                });
        },
        fetchCampaigns() {
            axios
                .get(`/api/influencer_api/influencer/${this.id}/campaigns`)
                .then((response) => {
                    this.campaigns = response.data;
                    this.totalCampaigns = this.campaigns.length;
                    this.activeCampaigns = this.campaigns.filter((campagin) => {
                        return campagin.Status === "Active";
                    }).length;
                    this.completedCampaigns = this.campaigns.filter(
                        (campagin) => {
                            return campagin.Status === "Completed";
                        }
                    ).length;
                    this.rejectedCampaigns = this.campaigns.filter(
                        (campagin) => {
                            return campagin.Status === "Rejected";
                        }
                    ).length;
                    console.log(typeof this.campaigns);
                    this.campaigns.map((campaign) => {
                        console.log(typeof campaign);
                        if (
                            campaign.Status === "Active" ||
                            campaign.Status === "Completed"
                        ) {
                            axios
                                .get(
                                    `/api/campaign_api/campaign/${campaign.Campaign_ID}/adrequest/${campaign.Ad_ID}/performance`
                                )
                                .then((response) => {
                                    console.log(response.data);
                                    this.totalReach += response.data.Reach;
                                    this.totalPosts += response.data.Posts;
                                    this.totalLikes += response.data.Likes;
                                })
                                .catch((error) => {
                                    console.error(
                                        "Error fetching campaigns:",
                                        error
                                    );
                                });
                        }
                    });
                })
                .catch((error) => {
                    console.error("Error fetching campaigns:", error);
                });
        },
        fetchAdPerformance(campaignId, adId) {
            return axios
                .get(
                    `/api/campaign_api/campaign/${campaignId}/adrequest/${adId}/performance`
                )
                .then((response) => {
                    return response.data;
                })
                .catch((error) => {
                    console.error("Error fetching ad performance:", error);
                });
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.fetchData();
        this.fetchCampaigns();
    },
});
