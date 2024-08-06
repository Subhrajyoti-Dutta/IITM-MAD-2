new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        position: "",
        loading: true,
        admins: [],
        modalAdmin: {},
        newAdmin: {
            Username: "",
            Password: "",
            Full_Name: "",
            Email: "",
            Position: "",
        },
    },
    methods: {
        openAddAdminModal() {
            this.newAdmin = {
                Username: "",
                Password: "",
                Full_Name: "",
                Email: "",
                Position: "",
            };
            $("#addAdminModal").modal("show");
        },
        addAdmin() {
            axios
                .post("/api/admin_api/admins", this.newAdmin)
                .then((response) => {
                    this.admins.push(response.data);
                    $("#addAdminModal").modal("hide");
                })
                .catch((error) => {
                    console.error("Error adding admin:", error);
                });
        },
        deleteAdmin(adminId) {
            axios
                .delete(`/api/admin_api/admin/${adminId}`)
                .then((response) => {
                    this.admins = this.admins.filter(
                        (admin) => admin.Admin_ID !== adminId
                    ); // delete admin from array
                    $("#addAdminModal").modal("hide");
                })
                .catch((error) => {
                    console.error("Error adding admin:", error);
                });
        },
        getData() {
            axios
                .get(`/api/admin_api/admin/${this.id}`)
                .then((response) => {
                    this.username = response.data.Username;
                    this.position = response.data.Position;
                })
                .catch((error) => {
                    console.error("Error fetching admin data:", error);
                    this.loading = false;
                });
        },
        fetchAdmins() {
            axios
                .get("/api/admin_api/admins")
                .then((response) => {
                    this.admins = response.data;
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching admins:", error);
                    this.loading = false;
                });
        },
        viewAdmin(admin) {
            this.modalAdmin = admin;
            $("#adminModal").modal("show");
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.getData();
        this.fetchAdmins();
    },
});
