<template>
  <h1>현재 위치</h1>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
      <form @submit.prevent="searchBank" style="display: flex; align-items: center; gap: 10px;">
        <select v-model="selectCity" class="form-select" aria-label="Default select example">
          <option value="0" selected>시 전체</option>
          <option v-for="city in Object.keys(cities)">{{ city }}</option>
        </select>
        <select v-model="selectState" class="form-select" aria-label="Default select example">
          <option value="0" selected>시/군/구</option>
          <option v-for="state in cities[selectCity]">{{ state }}</option>
        </select>
        <input type="submit" value="검색하기" class="btn btn-outline-primary"/>
      </form>
      <div class="btn-group" role="group" aria-label="Basic outlined example">
        <button @click="findbank" type="button" class="btn btn-outline-primary">은행 검색하기</button>
        <button @click="removebank" type="button" class="btn btn-outline-primary">검색 취소</button>
      </div>
    </div>
    <div id="map" style="width: 100%; height: 600px"></div>
  </div>
</template>

<script setup>
//현재 위치 정보 불러오기
import { ref, onMounted } from "vue";

const latitude = ref(35.2055289);
const longitude = ref(126.8115756);
const selectCity = ref("0")
const selectState = ref("0")


// 행정구 리스트
const cities = {
  '서울특별시':['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구',
    '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구'],
  '부산광역시':['중구', '서구', '동구', '영도구', '부산진구', '동래구', '남구', '북구', '강서구', '해운대구', '사하구', '금정구', '연제구', '수영구', '사상구', '기장군'],
  '대구광역시':['중구', '동구', '서구', '남구', '북구', '수성구', '달서구', '달성군', '군위군'],
  '인천광역시':['중구', '동구', '미추홀구', '연수구', '남동구', '부평구', '계양구', '서구', '강화군', '옹진군'],
  '광주광역시':['동구', '서구', '남구', '북구', '광산구'],
  '대전광역시':['동구', '중구', '서구', '유성구', '대덕구'],
  '울산광역시':['중구', '남구', '동구', '북구', '울주군'],
  '세종특별자치시':['세종시'],
  '경기도':['수원시', '성남시', '의정부시', '안양시', '부천시', '광명시', '동두천시', '평택시', '안산시', '고양시', '과천시', '구리시', '남양주시', '오산시',
    '시흥시', '군포시', '의왕시', '하남시', '용인시', '파주시', '이천시', '안성시', '김포시', '화성시', '광주시', '양주시', '포천시', '여주시',
    '연천군', '가평군', '양평군'],
  '강원도':['춘천시', '원주시', '강릉시', '동해시', '태백시', '속초시', '삼척시',
    '홍천군', '횡성군', '영월군', '평창군', '정선군', '철원군', '화천군', '양구군', '인제군', '고성군', '양양군'],
  '충청북도':['청주시', '충주시', '제천시',
    '보은군', '옥천군', '영동군', '증평군', '진천군', '괴산군', '음성군', '단양군'],
  '충청남도':['천안시', '공주시', '보령시', '아산시', '서산시', '논산시', '계릉시', '당진시',
    '금산군', '부여군', '서천군', '청양군', '홍성군', '예산군', '태안군'],
  '전라북도':['전주시', '군산시', '익산시', '정읍시', '남원시', '김제시',
    '완주군', '진안군', '무주군', '장수군', '임실군', '순창군', '고창군', '부안군'],
  '전라남도':['목포시', '여수시', '순천시', '나주시', '광양시',
    '담양군', '곡성군', '구례군', '고흥군', '보성군', '화순군', '장흥군', '강진군', '해남군', '영암군', '무안군', '함평군', '영광군', '장성군', '완도군', '진도군', '신안군'],
  '경상북도':['포항시', '경주시', '김천시', '안동시', '구미시', '영주시', '영천시', '상주시', '문경시', '경산시',
    '의성군', '청송군', '영양군', '영덕군', '청도군', '고령군', '성주군', '칠곡군', '예천군', '봉화군', '울진군', '울릉군'],
  '경상남도':['창원시', '진주시', '통영시', '사천시', '김해시', '밀양시', '거제시', '양산시',
    '의령군', '함안군', '창녕군', '고성군', '남해군', '하동군', '산청군', '함양군', '거창군', '합천군',],
  '제주특별자치도':['제주시', '서귀포시']
}

let map = null
let infowindow = null
let markers = ref([])

// KAKAO MAP API 불러오기
onMounted(() => {
  if (window.kakao?.maps) {
    initMap();
  } else {
    loadScript();
  }
});

const loadScript = () => {
  const KEY = import.meta.env.VITE_APP_KAKAO_JS_KEY;
  const script = document.createElement("script");
  script.type = "text/javascript";
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${KEY}&libraries=services,clusterer,drawing`;

  script.addEventListener("load", () => kakao.maps.load(initMap));

  document.head.appendChild(script);
};


function initMap() {
  kakao.maps.load(() => {
    const container = document.getElementById("map");

    const options = {
      center: new kakao.maps.LatLng(latitude.value, longitude.value),
      level: 5,
    };

    map = new kakao.maps.Map(container, options);

    const  markerPosition = new kakao.maps.LatLng(latitude.value, longitude.value); // 마커가 표시될 위치입니다

    // 마커를 생성합니다
    const marker = new kakao.maps.Marker({
      position: markerPosition,
    });

    // 마커가 지도 위에 표시되도록 설정합니다
    marker.setMap(map);

  });
}

const searchBank = function () {
  const geocoder = new kakao.maps.services.Geocoder();

  const callback = function(result, status) {
    if (status === kakao.maps.services.Status.OK) {
        console.log('result :', result);
        const position = new kakao.maps.LatLng(result[0].y, result[0].x);
        console.log('position :', position)
        map.panTo(position)
      }
  };

  geocoder.addressSearch(selectCity.value + selectState.value, callback);
}

function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {
      const bounds = new kakao.maps.LatLngBounds();
      markers.value = [];
      console.log('marker:', markers.value)
      for (let i = 0; i < data.length; i++) {
        const marker = displayMarker(data[i]);
        markers.value.push(marker);
        bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
      }
      map.setBounds(bounds);
    }
  }
  
function displayMarker(place) {
  const marker = new kakao.maps.Marker({
    map: map,
    position: new kakao.maps.LatLng(place.y, place.x)
  });

  infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });

  kakao.maps.event.addListener(marker, 'click', function() {
    infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
    infowindow.open(map, marker);
  });

  return marker;
}

function findbank () {
  markers.value.forEach(marker => {
    marker.setMap(null)
  });
  markers.value=[]

  const ps = new kakao.maps.services.Places(map)

  ps.categorySearch('BK9', placesSearchCB, {useMapBounds:true})
}

function removebank() {
  markers.value.forEach(marker => {
    marker.setMap(null)
  });
  markers.value=[]
}
</script>

<style scoped>

</style>