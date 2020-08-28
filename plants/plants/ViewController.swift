//
//  ViewController.swift
//  plants
//
//  Created by Ryan Goluch on 5/18/20.
//  Copyright © 2020 Ryan Goluch. All rights reserved.
//

import UIKit
import FLAnimatedImage
import SwiftGifOrigin
import Alamofire
import SwiftyJSON
import SwiftUI
import Charts
import TinyConstraints

class ViewController: UIViewController, ChartViewDelegate {
    @IBOutlet weak var dateLabel: UILabel!
    
    @IBOutlet weak var autoWaterStatus: UILabel!  //TODO: make this status change colors
    @IBOutlet weak var gifDisplay: UIImageView!
    @IBOutlet weak var watering_on: UIButton!
    @IBOutlet weak var watering_off: UIButton!
    
    var days = 0.0
    var showTrends: Bool = false
    var graph_data: JSON = []
    var moisture: [ChartDataEntry] = []
    var temp: [ChartDataEntry] = []
    @IBOutlet var waterDate: UILabel!
    @IBOutlet var waterTime: UILabel!
    
    
    lazy var lineChartView: LineChartView = {
        let chartView = LineChartView()
        
        chartView.backgroundColor = .init(displayP3Red: 0, green: 50, blue: 73, alpha: 0)
        chartView.rightAxis.enabled = false
        
        chartView.xAxis.labelPosition = .bottom
        chartView.xAxis.labelFont = .boldSystemFont(ofSize: 12)
        chartView.xAxis.labelTextColor = .white
        chartView.xAxis.axisLineColor = .white
        chartView.xAxis.valueFormatter = DateValueFormatter()
//        chartView.xAxis.setLabelCount(self.days, force: false)
        chartView.xAxis.granularityEnabled = true
        chartView.xAxis.granularity = self.days
        
        let y_axis = chartView.leftAxis
        y_axis.labelFont = .boldSystemFont(ofSize: 12)
        y_axis.setLabelCount(5, force: true)
        y_axis.labelTextColor = .white
        y_axis.axisLineColor = .white
        y_axis.labelPosition = .outsideChart
//        y_axis.granularityEnabled = true
//        y_axis.granularity = 3.0
        
        chartView.animate(xAxisDuration: 2.5)
        
        return chartView
    }()
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        let date = Date()
        let formatter = DateFormatter()
        formatter.dateFormat = "MM.dd.yyyy"
        dateLabel.text = formatter.string(from: date)
        get_last_water()
                
        if !showTrends{
            self.gifDisplay.image = UIImage.gif(name:"water5")
        } else{
            self.gifDisplay.isHidden = true
            show_trend_data()
        }
        
//        show_trend_data()
//        self.gifDisplay.isHidden = true
        lineChartView.isHidden = true
        view.addSubview(lineChartView)
        lineChartView.centerInSuperview()
        lineChartView.width(to: self.gifDisplay)
        lineChartView.height(to: self.gifDisplay)
        
        
        self.view.isUserInteractionEnabled = true
        
        
    }

    func chartValueSelected(_ chartView: ChartViewBase, entry: ChartDataEntry, highlight: Highlight) {
        print(entry)
    }
    
    func setData(){
        let set1 = LineChartDataSet(entries: self.moisture, label: "Plant Moisture")
        let set2 = LineChartDataSet(entries: self.temp, label: "Temperature")
        
        set1.drawCirclesEnabled = false
        set1.mode = .cubicBezier
        set1.lineWidth = 3
        set1.setColor(.white)
//        set1.fill = Fill(color: .white)
//        set1.fillAlpha = 0.8
        set1.drawFilledEnabled = true
        
        
        set2.drawCirclesEnabled = false
        set2.mode = .cubicBezier
        set2.lineWidth = 3
        set2.setColor(.green)
//        set2.fill = Fill(color: .green)
//        set2.fillAlpha = 0.8
        set2.drawFilledEnabled = true
        
        
        let data = LineChartData(dataSet: set1)
        let data2 = LineChartData(dataSet: set2)
        let data_set = LineChartData()
        data.setDrawValues(false)
        data2.setDrawValues(false)
        
        data_set.addDataSet(set1)
//        data_set.addDataSet(set2)
        
        lineChartView.data = data_set
    }
    
    @IBAction func watering_status(_ sender: Any) {
        print("water on!")
        AF.request("http://10.0.0.155:5000/water/on", method: .post).response{
                response in
            print (response)
        }
    }
    
    @IBAction func watering_status_off(_ sender: UIButton!) {
        AF.request("http://10.0.0.155:5000/water/off", method: .post).response{
                response in
            print (response)
        }
    }
    
    
    @IBAction func show_trend_data(){
        self.showTrends = true
        self.lineChartView.isHidden = false
        self.gifDisplay.isHidden = true

        let data = AF.request("http://10.0.0.155:5000/data", method: .get)
        data.responseJSON{ data_response in
            switch data_response.result{
            case .success(_):
//                print(JSON(data_response.data))
                self.graph_data = JSON(data_response.data!)
                var i = 0.0
                for (_, g) in self.graph_data{
                    if(g["m"] > 900.0){
                        continue
                    }
                    
                    let d = DateFormatter()
                    d.dateFormat = "MM.dd.yyyy"
                    var date_string = 0.0
                    date_string = d.date(from: g["date"].stringValue)!.timeIntervalSince1970
                    self.moisture.append(ChartDataEntry(x: date_string, y: g["m"].double!))
                    self.temp.append(ChartDataEntry(x: date_string, y: g["temp"].double!))
                    i+=1
//                    if (i == 15){
//                        break
//                    }
                }
                self.days = i/4
                print(i/4)
                self.setData()
                self.get_last_water()
            case .failure(_):
                print("No Data Retrieved")
            }
        }
    }

    
    func get_last_water(){
        let formatter = DateFormatter()
        formatter.dateFormat = "MM.dd.yyyy"
        
        
        let data = AF.request("http://10.0.0.155:5000/last_water", method: .get)
        data.responseJSON{ response in
            switch response.result{
            case .success(_):
                let x = JSON(response.data!)
                self.waterDate.text = "Last Water Date:\n" + x["date"].stringValue
                self.waterDate.sizeToFit()
                self.waterDate.textAlignment = .center
                self.waterDate.lineBreakMode = .byWordWrapping
                self.waterDate.numberOfLines = 2
                
                formatter.dateFormat = "HH:mm"
                self.waterTime.text = "Last Water Time:\n" + x["time"].stringValue
                self.waterTime.sizeToFit()
                self.waterTime.textAlignment = .center
                self.waterTime.lineBreakMode = .byWordWrapping
                self.waterTime.numberOfLines = 2
                
                
            case .failure(_):
                print("error")
            }
  
        }
        
    }
    
}

