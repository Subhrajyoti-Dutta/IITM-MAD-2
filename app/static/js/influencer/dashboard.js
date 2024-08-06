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
        modalCampaign: {},
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
        fetchAds(status) {
            return axios
                .get(
                    `/api/influencer_api/influencer/${this.id}/campaign/${status}`
                )
                .then((response) => {
                    return response.data;
                })
                .catch((error) => {
                    console.error(`Error fetching ${status} ads:`, error);
                    return [];
                });
        },
        viewCampaign(campaign) {
            this.modalCampaign = campaign;
            $("#campaignModal").modal("show");
        },
        acceptCampaign(campaignId, adRequestID) {
            axios
                .put(
                    `/api/campaign_api/campaign/${campaignId}/adrequest/${adRequestID}`,
                    {
                        Status: "Active",
                    }
                ) // Replace with actual endpoint
                .then((response) => {
                    console.log("Campaign accepted:", response);
                    this.fetchAds("null").then((data) => {
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
        rejectCampaign(campaignId, adRequestID) {
            axios
                .put(
                    `/api/campaign_api/campaign/${campaignId}/adrequest/${adRequestID}`,
                    {
                        Status: "Reject",
                    }
                ) // Replace with actual endpoint
                .then((response) => {
                    console.log("Campaign rejected:", response);
                    this.fetchAds("null").then((data) => {
                        this.newCampaigns = data;
                    });
                })
                .catch((error) => {
                    console.error("Error rejecting campaign:", error);
                });
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.fetchData();
        this.fetchAds("active").then((data) => {
            this.activeCampaigns = data;
        });
        // this.fetchAds("all").then((data) => {
        //     rate = 0;
        //     count = 0;
        //     data.forEach((campaign) => {
        //         if (
        //             campaign.Status === "Active" ||
        //             campaign.Status == "Completed"
        //         ) {
        //             axios
        //                 .get(
        //                     `/api/campaign_api/campaign/${campaign.Campaign_ID}/adrequest/${campaign.Ad_ID}/performance`
        //                 )
        //                 .then((response) => {
        //                     console.log(response.data);
        //                     rate = rate + response.data.Rating;
        //                     count = count + 1;
        //                     console.log(rate);
        //                     console.log(count);
        //                     this.averageRating =
        //                         Math.round((rate / count) * 100) / 100;
        //                 })
        //                 .catch((error) => {
        //                     console.error("Error rejecting campaign:", error);
        //                 });
        //         }
        //     });
        // });
        this.fetchAds("null").then((data) => {
            this.newCampaigns = data;
        });
    },
});
