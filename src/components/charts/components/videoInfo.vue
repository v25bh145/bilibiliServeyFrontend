<template>
    <v-card class="mx-auto" width="300px" height="400px" color="white">
        <v-card-title class="font-weight-black black--text ms-4">{{
            videoData.title
        }}</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
            <p>
                <span class="black--text ms-4">点赞量:</span>
                <span class="grey--text ms-4">{{ videoData.likes }}</span>
            </p>
            <p>
                <span class="black--text ms-4">投币量:</span>
                <span class="grey--text ms-4">{{ videoData.coins }}</span>
            </p>
            <p>
                <span class="black--text ms-4">播放量:</span>
                <span class="grey--text ms-4">{{ videoData.plays }}</span>
            </p>
            <p>
                <span class="black--text ms-4">UP主:</span>
                <span class="grey--text ms-4">
                    {{ videoData.UPName }}
                </span>
            </p>
            <!-- <p>
                <span class="black--text ms-4">视频更新时间:</span>
                <span class="grey--text ms-4">
                    {{ videoData.updateTime }}
                </span>
            </p> -->
            <p>
                <span class="black--text ms-4">视频所属专区:</span>
                <v-chip class="grey--text ms-4" @click="intoDepartmentVideo">{{
                    videoData.tName
                }}</v-chip>
            </p>
        </v-card-text>
    </v-card>
</template>
<script>
export default {
    props: ["videoData"],
    name: "videoInfo",
    data() {
        return {};
    },
    methods: {
        intoDepartmentVideo() {
            console.log("intoDepartmentVideo: " + this.videoData.tid);
            this.$emit("intoDepartmentVideo", {tid: this.videoData.tid, tName: this.videoData.tName});
        }
    }
};
</script>
