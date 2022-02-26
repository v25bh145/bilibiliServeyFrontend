<template>
    <!-- https://hub.fastgit.org/ecomfe/vue-echarts/blob/HEAD/README.zh-Hans.md -->
    <!-- 不同专区的投币/点赞[采样] -->
    <v-chart
        v-if="loading"
        :theme="theme"
        class="chart"
        :option="rateOption"
        @click="intoEvent"
    />
</template>

<script>
import { getDepartments } from "../../api/api";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { ScatterChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    VisualMapComponent,
} from "echarts/components";
import VChart from "vue-echarts";

use([
    CanvasRenderer,
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    VisualMapComponent,
    ScatterChart,
]);

export default {
    name: "DepartmentVideo",
    props: ["theme"],
    components: {
        VChart,
    },
    data() {
        return {
            rateData: [],
            loading: false,
            rateOption: {
                animationDelay: function (idx) {
                    // 越往后的数据延迟越大
                    return idx * 100;
                },
                title: {
                    text: "不同专区视频数据分析图",
                    left: "center",
                },
                tooltip: {
                    trigger: "item",
                    axisPointer: {
                        type: "cross",
                        snap: "true",
                    },
                    showContent: "true",
                    formatter(params) {
                        return (
                            "专区: " +
                            params.value[3] +
                            "<br>总投币 / 总点赞: " +
                            params.value[1] / params.value[0] +
                            "<br>总点赞量: " +
                            params.value[0] +
                            "<br>总投币量: " +
                            params.value[1] +
                            "<br>总视频数: " +
                            params.value[2]
                        );
                    },
                },
                legend: {
                    top: "5%",
                    left: "right",
                    type: "scroll",
                    width: "500px",
                    orient: "vertical",
                },
                visualMap: [
                    {
                        left: "83%",
                        top: "10%",
                        dimension: 2,
                        min: 0,
                        max: 0,
                        itemWidth: 30,
                        itemHeight: 120,
                        calculable: true,
                        precision: 0.1,
                        text: ["视频数"],
                        textGap: 20,
                        inRange: {
                            symbolSize: [10, 70],
                        },
                        outOfRange: {
                            symbolSize: [10, 70],
                            color: ["rgba(255,255,255,0.4)"],
                        },
                        controller: {
                            // inRange: {
                            //     color: ["#bbb"],
                            // },
                            outOfRange: {
                                color: ["#999"],
                            },
                        },
                    },
                ],
                xAxis: {
                    type: "value",
                    name: "点赞量",
                    nameTextStyle: {
                        color: "#0",
                    },
                    axisTick: {
                        alignWithLabel: true,
                    },
                },
                yAxis: {
                    type: "value",
                    name: "投币量",
                    nameTextStyle: {
                        color: "#0",
                    },
                },
                series: [
                    {
                        type: "scatter",
                        data: {},
                    },
                ],
            },
        };
    },
    methods: {
        intoEvent(params) {
            this.$emit("DepartmentsClick", params);
        },
        // getMaxPlays() {
        //     let rateData = this.rateData;
        //     let maxPlays = 0;
        //     for (let i in rateData)
        //         maxPlays =
        //             maxPlays > rateData[i][2] ? maxPlays : rateData[i][2];
        //     return maxPlays;
        // },
        // getRateData() {
        //     return [
        //         [900500, 55201, 413234300, "动画区/国创", "tid0"],
        //         [720404, 10012, 473200000, "生活区/萌宠", "tid1"],
        //         [540452, 12450, 124200000, "游戏区/单机游戏", "tid2"],
        //         [701520, 10055, 214000000, "游戏区/网络游戏", "tid2"],
        //         [701525, 10215, 320001400, "动画区/知识", "tid2"],
        //         [725153, 10221, 423200000, "时尚区/美妆护肤", "tid2"],
        //         [124507, 10150, 343225200, "运动区/健身", "tid2"],
        //         [455447, 44540, 466204200, "运动区/竞技体育", "tid2"],
        //         [123527, 14235, 200415000, "美食区/美食制作", "tid2"],
        //     ];
        // },
    },
    mounted() {
        let that = this;
        that.rateData = [];
        let data = getDepartments();
        let maxPlays = 0;
        data.then(function (data) {
            let dataArray = data.data.message;
            for (let i = 0; i < dataArray.length; ++i) {
                that.rateData.push([
                    dataArray[i].samples_likes,
                    dataArray[i].samples_coins,
                    dataArray[i].all_videos,
                    dataArray[i].name,
                    dataArray[i].tid,
                ]);
                maxPlays =
                    maxPlays > that.rateData[i][2]
                        ? maxPlays
                        : that.rateData[i][2];
            }
            that.rateOption.visualMap[0].max = maxPlays;
            that.rateOption.series[0].data = that.rateData;
            that.loading = true;
        });
    },
};
</script>

<style>
.chart {
    top: 25px;
    position: relative;
    height: 85%;
    width: 100%;
}
</style>
