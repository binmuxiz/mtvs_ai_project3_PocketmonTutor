console.log("🟡 renderer.js 실행됨")


import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'

const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
const renderer = new THREE.WebGLRenderer({ antialias: true })
renderer.setSize(window.innerWidth, window.innerHeight)
document.body.appendChild(renderer.domElement)

const light = new THREE.DirectionalLight(0xffffff, 1)
light.position.set(1, 1, 1).normalize()
scene.add(light)

const loader = new GLTFLoader()
loader.load('./pocketmon-model.glb', (gltf) => {
  console.log("✅ 모델 로딩 성공:", gltf)
  scene.add(gltf.scene)
}, undefined, (error) => {
  console.error('모델 로딩 실패:', error)
})

camera.position.z = 5

function animate() {
  requestAnimationFrame(animate)
  renderer.render(scene, camera)
}
animate()
