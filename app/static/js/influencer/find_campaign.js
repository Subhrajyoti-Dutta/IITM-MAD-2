new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        averageRating: 0,
        totalEarnings: 0,
        loading: true,
        searchQuery: "",
        selectedSponsor: "",
        selectedStatus: "all",
        startDate: "",
        endDate: "",
        campaigns: [],
        filteredCampaigns: [],
        sponsors: [],
    },
    methods: {
        fetchData() {
            axios
                .get("/api/influencer_api/influencer/1947380509")
                .then((response) => {
                    this.id = response.data["Influencer_ID"];
                    this.username = response.data["Username"];
                    this.averageRating = response.data["Average_Rating"];
                    this.totalEarnings = response.data["Total_Earnings"];
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                    this.loading = false;
                });
        },
        fetchSponsors() {
            axios
                .get("/api/sponsor_api/sponsors")
                .then((response) => {
                    this.sponsors = response.data;
                })
                .catch((error) => {
                    console.error("Error fetching sponsors:", error);
                });
        },
        fetchCampaigns() {
            axios
                .get("/api/campaign_api/campaigns")
                .then((response) => {
                    this.campaigns = response.data;
                    this.filteredCampaigns = response.data; // Initially display all campaigns
                })
                .catch((error) => {
                    console.error("Error fetching campaigns:", error);
                });
        },
        filterCampaigns() {
            this.filteredCampaigns = this.campaigns.filter((campaign) => {
                const matchesName = campaign.name
                    .toLowerCase()
                    .includes(this.searchQuery.toLowerCase());
                const matchesSponsor = this.selectedSponsor
                    ? campaign.sponsor_id == this.selectedSponsor
                    : true;
                const matchesStatus =
                    this.selectedStatus === "all" ||
                    campaign.status === this.selectedStatus;
                const matchesStartDate = this.startDate
                    ? new Date(campaign.start_date) >= new Date(this.startDate)
                    : true;
                const matchesEndDate = this.endDate
                    ? new Date(campaign.end_date) <= new Date(this.endDate)
                    : true;

                return (
                    matchesName &&
                    matchesSponsor &&
                    matchesStatus &&
                    matchesStartDate &&
                    matchesEndDate
                );
            });
        },
    },
    created() {
        this.fetchData();
        this.fetchSponsors();
        this.fetchCampaigns();
    },
});
