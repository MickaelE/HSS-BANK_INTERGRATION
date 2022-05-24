
package cam54;

import java.math.BigDecimal;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for ImpliedCurrencyAmountRangeChoice complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="ImpliedCurrencyAmountRangeChoice"&gt;
 *   &lt;complexContent&gt;
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType"&gt;
 *       &lt;sequence&gt;
 *         &lt;choice&gt;
 *           &lt;element name="FrAmt" type="{urn:iso:std:iso:20022:tech:xsd:camt.054.001.02}AmountRangeBoundary1"/&gt;
 *           &lt;element name="ToAmt" type="{urn:iso:std:iso:20022:tech:xsd:camt.054.001.02}AmountRangeBoundary1"/&gt;
 *           &lt;element name="FrToAmt" type="{urn:iso:std:iso:20022:tech:xsd:camt.054.001.02}FromToAmountRange"/&gt;
 *           &lt;element name="EQAmt" type="{urn:iso:std:iso:20022:tech:xsd:camt.054.001.02}ImpliedCurrencyAndAmount"/&gt;
 *           &lt;element name="NEQAmt" type="{urn:iso:std:iso:20022:tech:xsd:camt.054.001.02}ImpliedCurrencyAndAmount"/&gt;
 *         &lt;/choice&gt;
 *       &lt;/sequence&gt;
 *     &lt;/restriction&gt;
 *   &lt;/complexContent&gt;
 * &lt;/complexType&gt;
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "ImpliedCurrencyAmountRangeChoice", namespace = "urn:iso:std:iso:20022:tech:xsd:camt.054.001.02", propOrder = {
    "frAmt",
    "toAmt",
    "frToAmt",
    "eqAmt",
    "neqAmt"
})
public class ImpliedCurrencyAmountRangeChoice {

    @XmlElement(name = "FrAmt", namespace = "urn:iso:std:iso:20022:tech:xsd:camt.054.001.02")
    protected AmountRangeBoundary1 frAmt;
    @XmlElement(name = "ToAmt", namespace = "urn:iso:std:iso:20022:tech:xsd:camt.054.001.02")
    protected AmountRangeBoundary1 toAmt;
    @XmlElement(name = "FrToAmt", namespace = "urn:iso:std:iso:20022:tech:xsd:camt.054.001.02")
    protected FromToAmountRange frToAmt;
    @XmlElement(name = "EQAmt", namespace = "urn:iso:std:iso:20022:tech:xsd:camt.054.001.02")
    protected BigDecimal eqAmt;
    @XmlElement(name = "NEQAmt", namespace = "urn:iso:std:iso:20022:tech:xsd:camt.054.001.02")
    protected BigDecimal neqAmt;

    /**
     * Gets the value of the frAmt property.
     * 
     * @return
     *     possible object is
     *     {@link AmountRangeBoundary1 }
     *     
     */
    public AmountRangeBoundary1 getFrAmt() {
        return frAmt;
    }

    /**
     * Sets the value of the frAmt property.
     * 
     * @param value
     *     allowed object is
     *     {@link AmountRangeBoundary1 }
     *     
     */
    public void setFrAmt(AmountRangeBoundary1 value) {
        this.frAmt = value;
    }

    /**
     * Gets the value of the toAmt property.
     * 
     * @return
     *     possible object is
     *     {@link AmountRangeBoundary1 }
     *     
     */
    public AmountRangeBoundary1 getToAmt() {
        return toAmt;
    }

    /**
     * Sets the value of the toAmt property.
     * 
     * @param value
     *     allowed object is
     *     {@link AmountRangeBoundary1 }
     *     
     */
    public void setToAmt(AmountRangeBoundary1 value) {
        this.toAmt = value;
    }

    /**
     * Gets the value of the frToAmt property.
     * 
     * @return
     *     possible object is
     *     {@link FromToAmountRange }
     *     
     */
    public FromToAmountRange getFrToAmt() {
        return frToAmt;
    }

    /**
     * Sets the value of the frToAmt property.
     * 
     * @param value
     *     allowed object is
     *     {@link FromToAmountRange }
     *     
     */
    public void setFrToAmt(FromToAmountRange value) {
        this.frToAmt = value;
    }

    /**
     * Gets the value of the eqAmt property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getEQAmt() {
        return eqAmt;
    }

    /**
     * Sets the value of the eqAmt property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setEQAmt(BigDecimal value) {
        this.eqAmt = value;
    }

    /**
     * Gets the value of the neqAmt property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getNEQAmt() {
        return neqAmt;
    }

    /**
     * Sets the value of the neqAmt property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setNEQAmt(BigDecimal value) {
        this.neqAmt = value;
    }

}
