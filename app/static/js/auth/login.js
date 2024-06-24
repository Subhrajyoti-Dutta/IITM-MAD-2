new Vue({
    el: "#app",
    data: {
        username: "",
        password: "",
        remember: false,
        error: "",
    },
    methods: {
        login() {
            axios
                .post("/auth/login", {
                    username: this.username,
                    password: this.password,
                    remember: this.remember,
                })
                .then((response) => {
                    if (response.data.success) {
                        localStorage.setItem("id", response.data.id);
                        window.location.href = response.data.next || "/";
                    } else {
                        this.error = response.data.message;
                    }
                })
                .catch((error) => {
                    this.error = "An error occurred. Please try again.";
                });
        },
    },
});
