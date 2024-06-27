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
                    console.log(response.data);
                    this.username = response.data["Username"];
                    this.company = response.data["Company"];
                    // this.budget = response.data["Budget"];
                    this.loading = false;
                    console.log(this.loading);
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
            $("#campaignModal").modal("show");
        },
        deleteCampaign(campaignId) {
            axios
                .delete(`/api/campaign_api/campaign/${campaignId}`)
                .then((response) => {
                    console.log("Campaign deleted:", response);
                    this.fetchCampaigns("Pending").then((data) => {
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
        this.fetchCampaigns("active").then((data) => {
            this.activeCampaigns = data;
        });
        this.fetchCampaigns("null").then((data) => {
            this.pendingCampaigns = data;
        });
    },
});
