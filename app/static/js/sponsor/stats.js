new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        company: "",
        budget: 0,
        loading: true,
        campaigns: [],
    },
    methods: {
        fetchData() {
            axios
                .get(`/api/sponsor_api/sponsor/${this.id}`)
                .then((response) => {
                    this.username = response.data["Username"];
                    this.company = response.data["Company"];
                    this.budget = response.data["Budget"];
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                    this.loading = false;
                });
        },
        fetchCampaignStats() {
            axios
                .get(`/api/sponsor_api/sponsor/${this.id}/campaigns`)
                .then((response) => {
                    const campaigns = response.data;

                    const performancePromises = campaigns.map((campaign) => {
                        const adPromises = campaign.Ads.map((ad) =>
                            axios
                                .get(
                                    `/api/campaign_api/campaign/${campaign.Campaign_ID}/adrequest/${ad.Ad_ID}/performance`
                                )
                                .then((adResponse) => {
                                    const adPerformance = adResponse.data;
                                    ad.Reach = adPerformance.Reach || 0;
                                    ad.Posts = adPerformance.Posts || 0;
                                    ad.Likes = adPerformance.Likes || 0;
                                    ad.Rating = adPerformance.Rating || 0;
                                    return ad;
                                })
                                .catch((error) => {
                                    console.error(
                                        "Error fetching ad performance:",
                                        error
                                    );
                                    ad.Reach = 0;
                                    ad.Posts = 0;
                                    ad.Likes = 0;
                                    ad.Rating = 0;
                                    return ad;
                                })
                        );

                        return Promise.all(adPromises).then((ads) => {
                            let reach = 0,
                                posts = 0,
                                likes = 0,
                                rating = 0;
                            ads.forEach((ad) => {
                                reach += ad.Reach;
                                posts += ad.Posts;
                                likes += ad.Likes;
                                rating += ad.Rating;
                            });
                            campaign.Reach = reach;
                            campaign.Posts = posts;
                            campaign.Likes = likes;
                            campaign.Rating = (rating / ads.length).toFixed(2);
                            return campaign;
                        });
                    });

                    Promise.all(performancePromises)
                        .then((updatedCampaigns) => {
                            this.campaigns = updatedCampaigns;
                            console.log("Updated campaigns:", this.campaigns);
                        })
                        .catch((error) => {
                            console.error("Error updating campaigns:", error);
                        });
                })
                .catch((error) => {
                    console.error("Error fetching campaigns:", error);
                });
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.fetchData();
        this.fetchCampaignStats();
    },
});
