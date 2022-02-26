<template>
    <div>
        <v-app-bar app color="secondary" dark>
            <div class="d-flex align-center">
                <v-img
                    class="shrink mr-2"
                    contain
                    min-width="100"
                    src="../assets/bilibili.svg"
                    transition="scale-transition"
                    width="150"
                />
            </div>
            <v-btn
                class="mx-2"
                fab
                dark
                small
                color="primary"
                @click="backClicked"
            >
                <v-icon dark> mdi-arrow-left </v-icon>
            </v-btn>
            <v-spacer></v-spacer>

            <v-btn
                href=""
                target="_blank"
                text
                max-width="100"
                @click="UPs100BtnClicked"
            >
                <span class="mr-2">百大UP分析</span>
            </v-btn>
            <span class="mr-2">/</span>
            <v-btn
                href=""
                target="_blank"
                text
                max-width="75"
                @click="DepartmentsBtnClicked"
            >
                <span class="mr-2">专栏分析</span>
            </v-btn>
        </v-app-bar>
        <!-- 初始左边存第一个页面，不放页面 -->
        <div id="main-data">
            <div class="chart-data">
                <UPs100
                    :theme="theme"
                    class="chart-item"
                    v-if="currentLeftCharts == 'UPs100'"
                    @UPs100Click="UPs100Click"
                />
                <DepartmentVideo
                    :theme="theme"
                    class="chart-item"
                    v-if="currentLeftCharts == 'DepartmentVideo'"
                    :TID="TID"
                    :TName="TName"
                    @DepartmentVideoClick="DepartmentVideoClick"
                    @intoDepartmentVideo="intoDepartmentVideo"
                />
                <Departments
                    :theme="theme"
                    class="chart-item"
                    v-if="currentLeftCharts == 'Departments'"
                    @DepartmentsClick="DepartmentsClick"
                />
                <UPVideo
                    :theme="theme"
                    class="chart-item"
                    v-if="currentLeftCharts == 'UPVideo'"
                    :UID="UID"
                    :UPName="UPName"
                    @UPVideoClick="UPVideoClick"
                    @intoDepartmentVideo="intoDepartmentVideo"
                />
            </div>
            <div class="chart-data" v-if="currentRightCharts != null">
                <UPs100
                    :theme="theme"
                    class="chart-item"
                    v-if="currentRightCharts == 'UPs100'"
                    @UPs100Click="UPs100Click"
                />
                <DepartmentVideo
                    :theme="theme"
                    class="chart-item"
                    v-if="currentRightCharts == 'DepartmentVideo'"
                    :TID="TID"
                    :TName="TName"
                    @DepartmentVideoClick="DepartmentVideoClick"
                    @intoDepartmentVideo="intoDepartmentVideo"
                />
                <Departments
                    :theme="theme"
                    class="chart-item"
                    v-if="currentRightCharts == 'Departments'"
                    @DepartmentsClick="DepartmentsClick"
                />
                <UPVideo
                    :theme="theme"
                    class="chart-item"
                    v-if="currentRightCharts == 'UPVideo'"
                    :UID="UID"
                    :UPName="UPName"
                    @UPVideoClick="UPVideoClick"
                    @intoDepartmentVideo="intoDepartmentVideo"
                />
            </div>
        </div>
    </div>
</template>
<script>
import UPs100 from "../components/charts/UPs100";
import DepartmentVideo from "../components/charts/DepartmentVideo";
import Departments from "../components/charts/Departments";
import UPVideo from "../components/charts/UPVideo";
// let charts = ["UP100", "DepartmentVideo", "Departments", "UpVideo"];
export default {
    name: "Charts",
    data: () => ({
        // tmp value
        theme: "custom",
        UID: 0,
        UPName: "UP主a",
        TID: 1,
        TName: "专区a",
        // stack
        historyDataStack: [],
        historyLeftStack: [],
        historyRightStack: [],
        stackLength: 0,
        // chart name
        currentLeftCharts: "UPs100",
        currentRightCharts: null,
    }),
    components: {
        UPs100,
        DepartmentVideo,
        Departments,
        UPVideo,
    },
    methods: {
        UPs100BtnClicked() {
            if (
                this.currentLeftCharts != "UPs100" ||
                this.currentRightCharts != null
            )
                this.jumpTo("UPs100");
        },
        DepartmentsBtnClicked() {
            if (
                this.currentLeftCharts != "Departments" ||
                this.currentRightCharts != null
            )
                this.jumpTo("Departments");
        },
        backClicked() {
            let that = this;
            if (that.stackLength == 0) {
                this.$router.push({
                    path: "/",
                });
                return;
            }
            that.currentLeftCharts = null;
            that.currentRightCharts = null;
            setTimeout(() => {
                that.stackLength--;
                that.currentLeftCharts =
                    that.historyLeftStack[that.stackLength];
                that.currentRightCharts =
                    that.historyRightStack[that.stackLength];
                this.UID = that.historyDataStack[that.stackLength].UID;
                this.UPName = that.historyDataStack[that.stackLength].UPName;
                this.TID = that.historyDataStack[that.stackLength].TID;
                this.TName = that.historyDataStack[that.stackLength].TName;
                that.historyLeftStack[that.stackLength] =
                    that.historyRightStack[that.stackLength] = null;
            }, 100);
        },
        intoDepartmentVideo(params) {
            let that = this;
            this.TID = params.tid;
            this.TName = params.tName;
            let tmpLeft = that.currentLeftCharts;
            let tmpRight = that.currentRightCharts;
            that.currentLeftCharts = null;
            that.currentRightCharts = null;
            setTimeout(() => {
                that.historyLeftStack[that.stackLength] = tmpLeft;
                that.historyRightStack[that.stackLength] = tmpRight;
                that.historyDataStack[that.stackLength] = {
                    UID: that.UID,
                    UPName: that.UPName,
                    TID: that.TID,
                    TName: that.TName,
                };
                that.stackLength++;
                that.currentLeftCharts = "DepartmentVideo";
                that.currentRightCharts = null;
            }, 100);
        },
        UPs100Click(params) {
            this.UID = params.value[2];
            this.UPName = params.value[0];
            console.log(this.UID);
            // 如果右边有页面且UPs100位于左边，则只更新右边数据
            if (
                this.currentLeftCharts == "UPs100" &&
                this.currentRightCharts != null
            )
                this.rightJumpTo("UPVideo");
            else this.jumpTo("UPs100", "UPVideo");
        },
        UPVideoClick(params) {
            if (typeof params.data.bv == "undefined") this.bv = params.data[4];
            else this.bv = params.data.bv;
            console.log(this.bv);
        },
        DepartmentVideoClick(params) {
            this.bv = params.data[4];
            console.log(this.bv);
        },
        DepartmentsClick(params) {
            this.TID = params.data[4];
            this.TName = params.data[3];
            console.log(this.TID);
            // 如果右边有页面且departments位于左边，则只更新右边数据
            if (
                this.currentLeftCharts == "Departments" &&
                this.currentRightCharts != null
            )
                this.rightJumpTo("DepartmentVideo");
            else this.jumpTo("Departments", "DepartmentVideo", params);
        },
        rightJumpTo(right) {
            let that = this;
            let tmpRight = that.currentRightCharts;
            that.currentRightCharts = null;
            setTimeout(() => {
                that.historyLeftStack[that.stackLength] =
                    that.currentLeftCharts;
                that.historyRightStack[that.stackLength] = tmpRight;
                that.historyDataStack[that.stackLength] = {
                    UID: that.UID,
                    UPName: that.UPName,
                    TID: that.TID,
                    TName: that.TName,
                };
                that.stackLength++;
                that.currentRightCharts = right;
            }, 100);
        },
        jumpTo(left, right) {
            let that = this;
            if (typeof right == "undefined") right = null;
            let tmpLeft = that.currentLeftCharts;
            let tmpRight = that.currentRightCharts;
            that.currentLeftCharts = null;
            that.currentRightCharts = null;
            setTimeout(() => {
                that.historyLeftStack[that.stackLength] = tmpLeft;
                that.historyRightStack[that.stackLength] = tmpRight;
                that.historyDataStack[that.stackLength] = {
                    UID: that.UID,
                    UPName: that.UPName,
                    TID: that.TID,
                    TName: that.TName,
                };
                that.stackLength++;
                that.currentLeftCharts = left;
                that.currentRightCharts = right;
            }, 100);
        },
    },
    mounted() {
        if (typeof this.$route.query.chartName != "undefined")
            this.currentLeftCharts = this.$route.query.chartName;
    },
};
</script>
<style>
#main-data {
    position: absolute;
    height: 100%;
    width: 100%;
    display: flex;
}
#side-data {
    height: 100%;
    width: 300px;
    flex: 1;
}
.chart-data {
    height: 100%;
    width: 100%;
    /* flex: 5; */
}
@keyframes chartInitAnm {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
.chart-item {
    opacity: 0;
    animation-name: chartInitAnm;
    animation-duration: 0.5s;
    animation-direction: normal;
    animation-timing-function: ease-in;
    animation-fill-mode: forwards;
}
</style>
