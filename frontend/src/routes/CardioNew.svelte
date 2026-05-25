<script lang="ts">
  import { cardio, type CardioWorkoutCreate } from '../lib/stores/workouts.svelte'
  import { ApiError } from '../lib/api/client'
  import { navigate } from '../lib/router'
  import CardioForm from '../lib/components/CardioForm.svelte'
  import { showToast } from '../lib/stores/toast.svelte'

  let saving = $state(false)
  let error = $state<string | null>(null)

  async function handleSubmit(data: CardioWorkoutCreate) {
    saving = true
    error = null
    try {
      const workout = await cardio.create(data)
      showToast('Workout created')
      navigate('cardio-detail', { id: workout.id })
    } catch (e) {
      error = e instanceof ApiError ? e.detail : 'Failed to create workout'
    } finally {
      saving = false
    }
  }

  function handleCancel() {
    navigate('cardio')
  }
</script>

<div class="max-w-2xl mx-auto">
  <h1 class="text-2xl font-bold text-gray-800 mb-6">New Cardio Workout</h1>

  {#if error}
    <div class="text-red-600 text-sm bg-red-50 border border-red-200 rounded px-4 py-3 mb-4">{error}</div>
  {/if}

  <div class="bg-white rounded-xl shadow-sm border border-gray-100 px-2 py-3">
    <CardioForm onsubmit={handleSubmit} oncancel={handleCancel} />
  </div>

  {#if saving}
    <div class="text-gray-400 text-sm text-center mt-4">Saving...</div>
  {/if}
</div>
