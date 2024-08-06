new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        company: "",
        budget: 0,
        loading: true,
        activeCampaigns: [],
        pendingCampaigns: [],
        modalCampaign: {},
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
        fetchCampaigns(status) {
            return axios
                .get(`/api/sponsor_api/sponsor/${this.id}/campaign/${status}`)
                .then((response) => {
                    return response.data;
                })
                .catch((error) => {
                    console.error(`Error fetching ${status} campaigns:`, error);
                    return [];
                });
        },
        viewCampaign(campaign) {
            this.modalCampaign = campaign;
            console.log(this.modalCampaign);
            $("#campaignModal").modal("show");
        },
        deleteCampaign(campaignId, adId) {
            axios
                .delete(
                    `/api/campaign_api/campaign/${campaignId}/adrequest/${adId}`
                )
                .then((response) => {
                    this.fetchCampaigns("null").then((data) => {
                        this.pendingCampaigns = data;
                    });
                })
                .catch((error) => {
                    console.error("Error deleting campaign:", error);
                });
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.fetchData();
        this.fetchCampaigns("Active").then((data) => {
            data.forEach((campaign) => {
                console.log(campaign);
                campaign.Ads.map((ad) => {
                    ad.Flag = ad.Flag || campaign.Flag;
                    ad.Campaign_ID = campaign.Campaign_ID;
                });
                this.activeCampaigns = this.activeCampaigns.concat(
                    campaign.Ads
                );
            });
            console.log(this.activeCampaigns);
        });
        this.fetchCampaigns("Null").then((data) => {
            data.forEach((campaign) => {
                campaign.Ads.map((ad) => {
                    ad.Flag = ad.Flag || campaign.Flag;
                    ad.Campaign_ID = campaign.Campaign_ID;
                });
                this.pendingCampaigns = this.pendingCampaigns.concat(
                    campaign.Ads
                );
            });
        });
    },
});
