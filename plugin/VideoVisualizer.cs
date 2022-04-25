using UnityEngine;
using UnityEditor;
using System.IO;

public class VideoVisualizer : EditorWindow
{
    private Vector3Int _startPosition;
    private string _video_path = null;
    private string _gpxPath = null;
    private float _focal_length = 2.1f;
    private int _baseline = 120;
    private Vector3Int _visual_angle;

    [MenuItem("Tools/RoadVisualizer")]
    private static void ShowWindow()
    {
        var window = GetWindow<VideoVisualizer>();
        window.titleContent = new GUIContent("Road visualizer");
        window.Show();
    }

    private void OnGUI()
    {
        this._startPosition = EditorGUILayout.Vector3IntField("Start position", this._startPosition);
        EditorGUILayout.Space(12);

        EditorGUILayout.LabelField($"Stereo video: {this._video_path ?? "not selected"}");
        bool selectVideoFileClicked = GUILayout.Button("Select video file");
        if (selectVideoFileClicked) this._video_path = EditorUtility.OpenFilePanel("Select file", "", "mp4");

        EditorGUILayout.Space(2);

        EditorGUILayout.LabelField($"GPX: {this._gpxPath ?? "not selected"}");
        bool selectGPXFileClicked = GUILayout.Button("Select gpx file");
        if (selectGPXFileClicked) this._gpxPath = EditorUtility.OpenFilePanel("Select file", "", "gpx");

        EditorGUILayout.Space(2);

        EditorGUILayout.LabelField($"Camera:");
        this._focal_length = EditorGUILayout.FloatField("Focal length (mm)", this._focal_length);
        EditorGUILayout.Space(2);
        this._visual_angle = EditorGUILayout.Vector3IntField("Visual angle (horizontal, vertical, diagonal)", this._visual_angle);
        EditorGUILayout.Space(2);
        this._baseline = EditorGUILayout.IntField("Baseline (mm)", this._baseline);

        EditorGUILayout.Space(12);

        bool executingButtonClicked = GUILayout.Button("Execute");
        if (executingButtonClicked) this.onExecuteClick();
    }

    private void onExecuteClick()
    {
        if (this._gpxPath == null || this._video_path == null) { return; }
        EditorGUI.BeginDisabledGroup(true);
        int i = 0;
        while (i < 100000) { i += 1; }

        var passport: Process = new Process();
        passport.StartInfo.FileName = "passport.exe";
        passport.StartInfo.Arguments = path;
        passport.Start();
    }

    private void spawn(string name, Vector3 position)
    {
        Vector3 DefaultScale = new Vector3(1, 1, 1);
        switch (name)
        {
            case "traffic_light":
                this.spawnPrefab("traffic_signal", position, Quaternion.Euler(0, 90, 0), DefaultScale);
                break;
            case "road_sign":
                this.spawnPrefab("road_sign", position, Quaternion.Euler(0, 90, 0), DefaultScale);
                break;
            case "crosswalk":
                this.spawnPrefab("PedestrianСrossing", position, Quaternion.Euler(0, 0, 0), new Vector3(3F, 0.1F, 1F));
            case "bus_station":
                this.spawnPrefab("BusStation", position, Quaternion.Euler(0, 0, 0), new Vector3(3F, 0.1F, 1F));
            case "camera":
                this.spawnPrefab("Camera", position, Quaternion.Euler(0, 0, 0), new Vector3(3F, 0.1F, 1F));
            case "barrier":
                this.spawnPrefab("Barrier", position, Quaternion.Euler(0, 0, 0), new Vector3(3F, 0.1F, 1F));
                break;
            default:
                break;
        }
    }

    private void spawnPrefab(string resource, Vector3 position, Quaternion rotation, Vector3 scale)
    {
        Object prefab = Resources.Load(resource);
        GameObject t = (GameObject) Instantiate(prefab, position, rotation);
        t.transform.localScale = scale;
    }
}