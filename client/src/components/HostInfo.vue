<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Storage Info</h1>
        <hr>
        <h3>Combined Storage</h3>
        <div class="progress">
          <div class="progress-bar progress-bar-striped" role="progressbar" style="width: 53%" aria-valuenow="53" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
        <p> 7.17 TB used of 14.37 TB </p>
       <br> 
        <button type="button" class="btn btn-success btn-sm">Add Storage Location</button>
        <br><br>
        <div v-for="(host, index) in hosts" :key="index" class="card">
          <h5 class="card-header"> {{ host.host }}</h5>
            <div class="card-body">
              <h4 class="card-title">Total</h4>
              <div class="progress">
                <div class="progress-bar progress-bar-striped" role="progressbar" style="width: 10%" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
              <p class="card-text">{{ host.storage_devices.slice(-1)[0].space_available }} free of {{ host.storage_devices.slice(-1)[0].space_size }} </p>
              <hr>
              <!-- STORAGE DEVICE CARDS -->
              <div v-for="(device, index) in host.storage_devices" :key="index">
                <div v-if="index < host.storage_devices.length-1">
                <div class="card">
                  <h5 class="card-header">{{ device.filesystem }}</h5>
                  <div class="card-body">
                  <p class="card-text"><i>{{ device.mount_location }}</i></p>
                  <div class="progress">
                    <div v-if="parseFloat(device.space_percentage) > 80" class="progress-bar bg-danger" role="progressbar" :style="{ width: device.space_percentage }"  aria-valuenow="10" aria-valuemin="0" aria-valuemax="100">{{ device.space_percentage }}</div>
                    <div v-else-if="parseFloat(device.space_percentage) > 50" class="progress-bar bg-warning" role="progressbar" :style="{ width: device.space_percentage }"  aria-valuenow="10" aria-valuemin="0" aria-valuemax="100">{{ device.space_percentage }}</div>
                    <div v-else class="progress-bar" role="progressbar" :style="{ width: device.space_percentage }"  aria-valuenow="10" aria-valuemin="0" aria-valuemax="100">{{ device.space_percentage }}</div>
                  </div>
                  <p class="card-text">{{ device.space_available }} free of {{ device.space_size }} </p>
                </div>
                </div>
                </div>
                <br>
              </div>
              <!-- END CARD -->
            </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      hosts: [],
    };
  },
  methods: {
    getHosts() {
      const path = 'http://172.26.201.124:5000/host-info';
      axios.get(path)
        .then((res) => {
          this.hosts = res.data.hosts;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getHosts();
  },
};
</script>