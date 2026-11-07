extends SceneTree

# Validate the delivered GLB with Godot's own importer and instantiate the result.
func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	GLTFDocument.register_gltf_document_extension(GLTFDocumentExtensionConvertImporterMesh.new())
	var doc := GLTFDocument.new()
	var state := GLTFState.new()
	if args.size() != 2 or doc.append_from_file(args[0], state) != OK:
		push_error("GLB load failed")
		quit(2)
		return
	var scene := doc.generate_scene(state)
	if scene == null:
		push_error("GLB scene is null")
		quit(2)
		return
	root.add_child(scene)
	var meshes := scene.find_children("*", "MeshInstance3D", true, false)
	if scene is MeshInstance3D:
		meshes.append(scene)
	if meshes.size() != 1:
		push_error("Expected exactly one mesh node")
		quit(2)
		return
	var node: MeshInstance3D = meshes[0]
	var mesh := node.mesh
	if mesh == null or mesh.get_surface_count() != 1:
		push_error("Expected one mesh surface")
		quit(2)
		return
	var mat := mesh.surface_get_material(0) as StandardMaterial3D
	if mat == null or mesh.surface_get_primitive_type(0) != Mesh.PRIMITIVE_TRIANGLES:
		push_error("Expected a PBR triangle surface")
		quit(2)
		return
	var bounds: AABB = node.transform * mesh.get_aabb()
	var size := bounds.size
	var result := {"engine": Engine.get_version_info().string, "size_m": [size.x, size.y, size.z],
		"floor_m": bounds.position.y, "triangles": mesh.get_faces().size() / 3,
		"material": mat.resource_name, "albedo": mat.albedo_color.to_html(false),
		"metallic": mat.metallic, "roughness": mat.roughness}
	var out := FileAccess.open(args[1], FileAccess.WRITE)
	if out == null:
		push_error("Could not write Godot report")
		quit(2)
		return
	out.store_string(JSON.stringify(result, "  "))
	out.close()
	scene.free()
	quit(0)
